#!/usr/bin/env python3
"""
Fill PDF form fields with provided data.

Usage:
  List fields:   python fill_pdf.py --list-fields input.pdf
  Fill form:     python fill_pdf.py --fill input.pdf output.pdf --data '{"field": "value"}'
  Fill from file: python fill_pdf.py --fill input.pdf output.pdf --data-file mappings.json
"""

import argparse
import json
import subprocess
import sys


def ensure_pypdf():
    """Install pypdf if not already available."""
    try:
        import pypdf  # noqa: F401
    except ImportError:
        print("Installing pypdf...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "pypdf", "-q"],
            stdout=subprocess.DEVNULL,
        )


def list_fields(input_path):
    """List all fillable form fields in a PDF."""
    from pypdf import PdfReader

    reader = PdfReader(input_path)
    fields = reader.get_fields()

    if not fields:
        print(json.dumps({"fields": [], "message": "No fillable form fields found in this PDF."}))
        return

    result = []
    for name, field in fields.items():
        field_info = {
            "name": name,
            "type": field.get("/FT", "unknown"),
            "current_value": field.get("/V", ""),
        }
        # Include dropdown/checkbox options if available
        if "/Opt" in field:
            field_info["options"] = field["/Opt"]
        result.append(field_info)

    print(json.dumps({"fields": result}, indent=2, default=str))


def fill_form(input_path, output_path, data):
    """Fill PDF form fields with the provided data mapping."""
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(input_path)
    writer = PdfWriter()
    writer.append(reader)

    filled_count = 0
    skipped = []

    for page_num in range(len(writer.pages)):
        page = writer.pages[page_num]
        if "/Annots" not in page:
            continue

        for annotation in page["/Annots"]:
            annot = annotation.get_object()
            field_name = annot.get("/T")
            if field_name and str(field_name) in data:
                writer.update_page_form_field_values(
                    page,
                    {str(field_name): data[str(field_name)]},
                )
                filled_count += 1

    # Also try the top-level update method for fields not caught per-page
    try:
        writer.update_page_form_field_values(
            writer.pages[0],
            data,
        )
    except Exception:
        pass

    with open(output_path, "wb") as f:
        writer.write(f)

    # Report what happened
    all_fields = reader.get_fields() or {}
    field_names = set(all_fields.keys())
    provided_keys = set(data.keys())
    matched = provided_keys & field_names
    not_found = provided_keys - field_names

    result = {
        "output": output_path,
        "total_form_fields": len(field_names),
        "fields_filled": len(matched),
        "fields_not_found_in_pdf": list(not_found),
        "available_fields": list(field_names),
    }
    print(json.dumps(result, indent=2, default=str))


def main():
    parser = argparse.ArgumentParser(description="Fill PDF form fields.")
    parser.add_argument("input_pdf", help="Path to the input PDF")
    parser.add_argument("output_pdf", nargs="?", help="Path for the output PDF (required with --fill)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--list-fields", action="store_true", help="List all fillable fields")
    group.add_argument("--fill", action="store_true", help="Fill form fields")

    parser.add_argument("--data", help="JSON string of field name to value mappings")
    parser.add_argument("--data-file", help="Path to JSON file with field mappings")

    args = parser.parse_args()

    ensure_pypdf()

    if args.list_fields:
        list_fields(args.input_pdf)
    elif args.fill:
        if not args.output_pdf:
            parser.error("--fill requires an output PDF path")
        if not args.data and not args.data_file:
            parser.error("--fill requires --data or --data-file")

        if args.data_file:
            with open(args.data_file) as f:
                data = json.load(f)
        else:
            data = json.loads(args.data)

        fill_form(args.input_pdf, args.output_pdf, data)


if __name__ == "__main__":
    main()
