#SVG Generaor for the Debt Payment Juorney Summary#

from datetime import datetime
from pathlib import Path

MIN_VISIBLE_ROWS = 3
MAX_VISIBLE_ROWS = 15


def format_money(amount):
    return f"P{amount:,.2f}"


def get_status(total_debt, total_paid):
    if total_debt <= 0:
        return "Fresh Start!"

    progress = total_paid / total_debt

    if total_paid == 0:
        return "Almost there."
    if progress < 0.15:
        return "Momentum."
    if progress < 0.40:
        return "On-track."
    if progress < 0.70:
        return "Strong!"
    if progress < 0.90:
        return "Excellent!"
    return "Victory!"

def generate_svg_summary(debt_records):
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    generated_at = datetime.now()
    timestamp = generated_at.strftime("%Y%m%d-%H%M%S")
    readable_timestamp = generated_at.strftime("%b %d, %Y, %I:%M %p")
    output_path = output_dir / f"debt-tracker-{timestamp}.svg"

    if not debt_records:
        rows_html = """
        <text x="450" y="350" text-anchor="middle" font-size="28" font-family="Segoe UI, Arial, sans-serif" fill="#5f6985" font-weight="700">No debts recorded yet</text>
        <text x="450" y="390" text-anchor="middle" font-size="18" font-family="Segoe UI, Arial, sans-serif" fill="#7685a6">Add your first debt to start tracking</text>
        """
        total_debt = 0.0
        total_paid = 0.0
        remaining_balance = 0.0
        status = "Fresh start"
        visible_rows = MIN_VISIBLE_ROWS
        extra_entries = 0
        extra_space = 0
    else:
        total_debt = sum(record["original_debt"] for record in debt_records.values())
        total_paid = sum(record["amount_paid"] for record in debt_records.values())
        remaining_balance = total_debt - total_paid
        status = get_status(total_debt, total_paid)

        visible_rows = min(max(len(debt_records), MIN_VISIBLE_ROWS), MAX_VISIBLE_ROWS)
        extra_entries = max(0, len(debt_records) - MAX_VISIBLE_ROWS)
        extra_space = max(0, visible_rows - MIN_VISIBLE_ROWS) * 48
        display_records = dict(list(debt_records.items())[:visible_rows])

        row_html = []
        for index, (bank_name, record) in enumerate(display_records.items()):
            current_balance = record["original_debt"] - record["amount_paid"]
            row_y = 350 + index * 48
            row_html.append(
                f"""
                <line x1="118" y1="{row_y}" x2="774" y2="{row_y}" stroke="#edf2fb" stroke-width="1.5"/>
                <text x="150" y="{row_y + 30}" class="cell" text-anchor="middle">{bank_name}</text>
                <text x="345" y="{row_y + 30}" class="money" text-anchor="middle">{format_money(record['original_debt'])}</text>
                <text x="517" y="{row_y + 30}" class="money" text-anchor="middle">{format_money(record['amount_paid'])}</text>
                <text x="689" y="{row_y + 30}" class="money" text-anchor="middle">{format_money(current_balance)}</text>
                """
            )

        if extra_entries > 0:
            extra_y = 350 + visible_rows * 48
            row_html.append(
                f"""
                <line x1="118" y1="{extra_y}" x2="774" y2="{extra_y}" stroke="#edf2fb" stroke-width="1.5"/>
                <text x="450" y="{extra_y + 30}" class="note" text-anchor="middle">+{extra_entries} more entries</text>
                """
            )

        rows_html = "\n".join(row_html)

    svg_height = 600 + extra_space
    card_height = 520 + extra_space
    table_height = 210 + extra_space
    total_box_y = 486 + extra_space
    footer_y = 560 + extra_space

    svg_content = f"""<svg width="900" height="{svg_height}" viewBox="0 0 900 {svg_height}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc">
  <title id="title">My Journey to a Debt-Free Future</title>
  <desc id="desc">A debt summary showing bank, debt amount, paid amount, and remaining balance.</desc>

  <defs>
    <linearGradient id="bgGrad" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#fdf2f8"/>
      <stop offset="100%" stop-color="#eef6ff"/>
    </linearGradient>
    <linearGradient id="cardGrad" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="#f7fbff" stop-opacity="0.95"/>
    </linearGradient>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#a7b4d8" flood-opacity="0.25"/>
    </filter>
    <style>
      .title {{ font: 700 30px 'Segoe UI', Arial, sans-serif; fill: #3d4a6a; }}
      .subtitle {{ font: 600 15px 'Segoe UI', Arial, sans-serif; fill: #6c7a9d; }}
      .label {{ font: 700 14px 'Segoe UI', Arial, sans-serif; fill: #52627d; }}
      .cell {{ font: 600 15px 'Segoe UI', Arial, sans-serif; fill: #2f3d59; }}
      .money {{ font: 700 15px 'Segoe UI', Arial, sans-serif; fill: #305a8c; }}
      .total {{ font: 800 15px 'Segoe UI', Arial, sans-serif; fill: #234b43; }}
      .badge {{ font: 700 12px 'Segoe UI', Arial, sans-serif; fill: #ffffff; }}
      .stamp {{ font: 600 12px 'Segoe UI', Arial, sans-serif; fill: #69789a; }}
      .note {{ font: 600 18px 'Segoe UI', Arial, sans-serif; fill: #5e6d8f; }}
    </style>
  </defs>

  <rect width="900" height="{svg_height}" fill="url(#bgGrad)"/>

  <g filter="url(#shadow)">
    <rect x="60" y="40" width="780" height="{card_height}" rx="28" fill="url(#cardGrad)"/>
  </g>

  <g>
    <circle cx="108" cy="100" r="26" fill="#ffd7e8"/>
    <circle cx="136" cy="78" r="14" fill="#ffe9b3"/>
    <rect x="90" y="125" width="28" height="56" rx="14" fill="#dfe8ff"/>
    <rect x="126" y="110" width="24" height="71" rx="12" fill="#d6f1e9"/>
    <rect x="156" y="118" width="24" height="63" rx="12" fill="#ffe7c5"/>

    <text x="190" y="104" class="title">My Journey to a Debt-Free Future</text>
    <text x="190" y="132" class="subtitle">A python application by EngrMyla</text>

    <ellipse cx="770" cy="102" rx="58" ry="22" fill="#cfe8ff"/>
    <text x="770" y="108" class="badge" text-anchor="middle">{status}</text>
    <text x="770" y="140" class="stamp" text-anchor="middle">as of {readable_timestamp}</text>
  </g>

  <g>
    <rect x="96" y="170" width="180" height="72" rx="18" fill="#dfeaff"/>
    <rect x="290" y="170" width="180" height="72" rx="18" fill="#dff6ec"/>
    <rect x="484" y="170" width="180" height="72" rx="18" fill="#fff0d6"/>
    <rect x="678" y="170" width="180" height="72" rx="18" fill="#f7dfee"/>

    <text x="116" y="197" class="label">Total Debt</text>
    <text x="116" y="220" class="money">{format_money(total_debt)}</text>

    <text x="310" y="197" class="label">Total Paid</text>
    <text x="310" y="220" class="money">{format_money(total_paid)}</text>

    <text x="504" y="197" class="label">Remaining</text>
    <text x="504" y="220" class="money">{format_money(remaining_balance)}</text>

    <text x="698" y="197" class="label">Entries</text>
    <text x="698" y="220" class="money">{len(debt_records)}{' bank' if len(debt_records) == 1 else ' banks' if len(debt_records) != 0 else ' banks'}</text>
  </g>

  <g>
    <rect x="96" y="270" width="708" height="{table_height}" rx="20" fill="#ffffff" opacity="0.8"/>

    <rect x="118" y="290" width="140" height="28" rx="14" fill="#e7edff"/>
    <text x="150" y="309" class="label" text-anchor="middle">Bank</text>

    <rect x="260" y="290" width="170" height="28" rx="14" fill="#eaf8f0"/>
    <text x="345" y="309" class="label" text-anchor="middle">Debt</text>

    <rect x="432" y="290" width="170" height="28" rx="14" fill="#fff0d6"/>
    <text x="517" y="309" class="label" text-anchor="middle">Paid</text>

    <rect x="604" y="290" width="170" height="28" rx="14" fill="#fbe5f2"/>
    <text x="689" y="309" class="label" text-anchor="middle">Balance</text>

    <line x1="118" y1="324" x2="774" y2="324" stroke="#dfe5f4" stroke-width="2"/>

    {rows_html}

    <line x1="118" y1="{350 + visible_rows * 48}" x2="774" y2="{350 + visible_rows * 48}" stroke="#dfe5f4" stroke-width="2"/>

    <rect x="604" y="{total_box_y}" width="170" height="34" rx="17" fill="#dff6ec"/>
    <text x="689" y="{total_box_y + 22}" class="total" text-anchor="middle">{format_money(remaining_balance)}</text>
  </g>

  <g>
    <text x="450" y="{footer_y}" text-anchor="middle" class="note">Yeeeyyy! I'm on my way to financial independence. Keep going — I've got this! ✨💛</text>
  </g>
</svg>
"""

    output_path.write_text(svg_content, encoding="utf-8")
    print(f"SVG summary saved to: {output_path}")
    return output_path