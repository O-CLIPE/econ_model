def print_in_file(filename: str, data: list, column_size_limit: int, headings: tuple):
    """Writes in filename.txt the data with headings and custom column_size."""
    with open(f"{filename}.txt", "w") as f:
        f.write("-- This was an automatically generated file. --\nData: ")
        for idx, head in enumerate(headings):
            f.write(f"{head}")
            if idx != len(headings) - 1:
                f.write(", ")
            else:
                f.write(".")
        f.write('\n\n')
        data.insert(0, headings)
        for table in data:
            for idx, column in enumerate(table):
                text = str(column)
                if len(text) >= column_size_limit - 2:
                    text = abbreviate(text, column_size_limit - 1)
                f.write(text)
                for i in range(column_size_limit - len(text)):
                    f.write(' ')
            f.write('\n')


def abbreviate(text: str, limit: int) -> str:
    """Abbreviate text to fit in limit."""
    abbr = str(text)
    for (old, new) in (("Incorporated", "Inc."), ("Company", "Co."), ("Limited", "Ltd."),
                       ("Association", "Assoc."), ("Brothers", "Bros."), ("Compagnie", "Cie."),
                       ("Manufacturings", "Mfg."), ("Manufacturers", "Mfrs.")):
        abbr = abbr.replace(old, new)

    if " " in text and len(abbr) > limit:
        if abbr.count(" ") <= limit/3:
            m = abbr.split()
            for idx, item in enumerate(m):
                if len(m[idx]) > 3:
                    m[idx] = f"{item[:3]}."
            abbr = " ".join(m)
        else:
            m = abbr.split()
            for idx, item in enumerate(m):
                m[idx] = item[0]
            abbr = "".join(m)
    elif len(abbr) > limit:
        abbr = f"{text[:limit - 1]}."
    return abbr[:limit]
