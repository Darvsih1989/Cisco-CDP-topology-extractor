ip}")
        continue

    for n in neighbors:
        sheet[f"A{row_counter}"] = ip
        sheet[f"B{row_counter}"] = platform
        sheet[f"C{row_counter}"] = n[0]
        sheet[f"D{row_counter}"] = n[1]
        sheet[f"E{row_counter}"] = n[2]
        sheet[f"F{row_counter}"] = n[3]
        sheet[f"G{row_counter}"] = n[3]
        row_counter += 1

# ---------------------------------------------------------------------------
# Auto-adjust column widths
# ---------------------------------------------------------------------------
for col in sheet.columns:
    max_len = 0
    col_letter = col[0].column_letter
    for cell in col:
        if cell.value:
            cell_len = len(str(cell.value))
            if cell_len > max_len:
                max_len = cell_len
    sheet.column_dimensions[col_letter].width = max_len + 2

# ---------------------------------------------------------------------------
# Save Excel
# ---------------------------------------------------------------------------
outfile = os.path.join(output_dir, "device_info.xlsx")
workbook.save(outfile)

print(f"\n✅ Extraction complete! Saved to: {outfile}")
