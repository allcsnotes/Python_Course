import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from fpdf import FPDF


def draw_chart(summary, path):
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
    per_course = summary.per_course
    ax.bar(
        per_course.index, per_course.revenue, color="#1a7cff"
    )
    ax.set_title("Revenue per course (Rs)")
    ax.tick_params(axis="x", labelrotation=20)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def line(pdf, text):
    pdf.cell(0, 9, text, new_x="LMARGIN", new_y="NEXT")


def build_pdf(summary, label, chart, path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    line(pdf, f"allcsvideos weekly report {label}")
    pdf.set_font("Helvetica", size=13)
    line(
        pdf,
        f"{summary.enrollments} new enrollments "
        f"(last week {summary.before})",
    )
    line(
        pdf,
        f"Revenue Rs {summary.gross}, refunds "
        f"Rs {summary.refunded}, net Rs {summary.net}",
    )
    line(pdf, f"Top course: {summary.per_course.index[0]}")
    pdf.image(str(chart), x=10, w=190)
    pdf.output(str(path))
