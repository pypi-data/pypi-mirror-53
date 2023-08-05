# l2q - List to Query

## Installing

```bash
pip install l2q
```

## Running

Given an Excel spreadsheet with the contents:

<table>
    <tr>
        <th></th>
        <th>A</th>
    </tr>
    <tr>
        <th>1</th>
        <td>blue</td>
    </tr>
    <tr>
        <th>2</th>
        <td>black</td>
    </tr>
    <tr>
        <th>3</th>
        <td>silver</td>
    </tr>
    <tr>
        <th>4</th>
        <td>white</td>
    </tr>
</table>

Running the command:

```bash
$ l2q terms.xlsx
blue OR black OR silver OR white
```

`l2q` also works with Word files (.docx) and text files.