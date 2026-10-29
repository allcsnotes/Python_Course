from payments import make_gateway

gateway = make_gateway("upi")
print(type(gateway).__name__)
print(gateway.charge("Lukas", 590))
make_gateway("crypto")
