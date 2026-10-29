#!/usr/bin/env bash
# Builds a throwaway git repository "bisect_repo" with 17 commits for the git bisect demo.
# Run it from an empty scratch folder. Uses local git config only. Written for macOS (sed -i ''); on Linux replace with sed -i.
set -e
rm -rf bisect_repo; mkdir bisect_repo; cd bisect_repo
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_NOSYSTEM=1
git init -q -b main
git config user.name "Asha"; git config user.email "asha@example.com"; git config commit.gpgsign false; git config core.hooksPath /dev/null
n=0
c() { n=$((n+1)); local d=$(printf "2026-10-%02dT10:00:00" $((n+9))); GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git add -A && GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git commit -q -m "$1"; }
cat > check.py <<'EOF'
from cart import total

result = total([1500, 500, 500], 10)
print(result)
raise SystemExit(0 if result == 2655 else 1)
EOF
cat > cart.py <<'EOF'
def total(prices, percent):
    return sum(prices)
EOF
c "Add the cart total"
cat > cart.py <<'EOF'
def total(prices, percent):
    subtotal = sum(prices)
    discount = subtotal * percent // 100
    return subtotal - discount
EOF
c "Take a percent coupon off"
cat > cart.py <<'EOF'
def total(prices, percent):
    subtotal = sum(prices)
    discount = subtotal * percent // 100
    tax = (subtotal - discount) * 18 // 100
    return subtotal - discount + tax
EOF
c "Add 18 percent GST"
echo "# cart" > README.md; c "Add a README"
sed -i '' 's/subtotal/before_coupon/g' cart.py; c "Rename subtotal to before_coupon"
echo "Totals are in whole rupees." >> README.md; c "Note whole rupees in the README"
sed -i '' 's/before_coupon/subtotal/g' cart.py; c "Rename it back to subtotal"
cat > cart.py <<'EOF'
def total(prices, percent):
    """Total in rupees for a list of prices."""
    subtotal = sum(prices)
    discount = subtotal * percent // 100
    tax = (subtotal - discount) * 18 // 100
    return subtotal - discount + tax
EOF
c "Add a docstring"
echo "Run check.py to test the total." >> README.md; c "Explain check.py"
cat > cart.py <<'EOF'
GST_PERCENT = 81


def total(prices, percent):
    """Total in rupees for a list of prices."""
    subtotal = sum(prices)
    discount = subtotal * percent // 100
    tax = (subtotal - discount) * GST_PERCENT // 100
    return subtotal - discount + tax
EOF
c "Move the GST rate into a constant"
echo "GST is set in cart.py." >> README.md; c "Say where GST is set"
cat > cart.py <<'EOF'
GST_PERCENT = 81


def total(prices, percent):
    """Total in rupees for a list of prices."""
    subtotal = sum(prices)
    discount = subtotal * percent // 100
    taxable = subtotal - discount
    tax = taxable * GST_PERCENT // 100
    return taxable + tax
EOF
c "Name the taxable amount"
echo "Coupons are percents." >> README.md; c "Mention coupons"
sed -i '' 's/Total in rupees/The total in rupees/' cart.py; c "Reword the docstring"
echo "Questions go to Asha." >> README.md; c "Add a contact line"
printf '\n\ndef flat(prices, off):\n    return sum(prices) - off\n' >> cart.py; c "Add a flat coupon helper"
echo "Flat coupons come later." >> README.md; c "Note flat coupons"

