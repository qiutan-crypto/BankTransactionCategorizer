import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime
import time
import os

# GUI App
class QBOConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel to QBO Converter")
        self.root.geometry("420x300")

        self.label = tk.Label(root, text="Select Excel File (with Schedule C classification):")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Browse Excel File", command=self.select_file)
        self.select_button.pack(pady=5)

        self.acctid_label = tk.Label(root, text="Enter last 4 digits of account:")
        self.acctid_label.pack(pady=5)
        self.acctid_entry = tk.Entry(root)
        self.acctid_entry.pack(pady=2)

        self.account_type = tk.StringVar(value="BANK")
        self.radio_frame = tk.Frame(root)
        self.radio_label = tk.Label(self.radio_frame, text="Account Type:")
        self.radio_label.pack(side=tk.LEFT)
        self.bank_radio = tk.Radiobutton(self.radio_frame, text="Bank (Checking)", variable=self.account_type, value="BANK")
        self.bank_radio.pack(side=tk.LEFT, padx=5)
        self.cc_radio = tk.Radiobutton(self.radio_frame, text="Credit Card", variable=self.account_type, value="CREDITCARD")
        self.cc_radio.pack(side=tk.LEFT)
        self.radio_frame.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert to QBO", command=self.convert_file, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.file_path = None

    def select_file(self):
        filetypes = [("Excel files", "*.xlsx *.xls")]
        self.file_path = filedialog.askopenfilename(title="Open Excel File", filetypes=filetypes)
        if self.file_path:
            self.convert_button.config(state=tk.NORMAL)
            messagebox.showinfo("File Selected", f"File selected:\n{self.file_path}")

    def convert_file(self):
        try:
            acct_last4 = self.acctid_entry.get().strip()
            if not acct_last4.isdigit() or len(acct_last4) != 4:
                raise ValueError("Please enter a valid 4-digit account number suffix.")

            acct_type = self.account_type.get()
            acct_id = f"391892{acct_last4}" if acct_type == "BANK" else f"424631531823{acct_last4}"

            df = pd.read_excel(self.file_path)
            required_columns = ["Date", "Description", "Amount", "Schedule C Category"]
            if not all(col in df.columns for col in required_columns):
                raise ValueError("Excel must contain columns: Date, Description, Amount, Schedule C Category")

            now = datetime.now().strftime("%Y%m%d%H%M%S")
            dtstart = pd.to_datetime(df["Date"]).min().strftime("%Y%m%d")
            dtend = pd.to_datetime(df["Date"]).max().strftime("%Y%m%d")
            timestamp_suffix = str(int(time.time()))[-6:]

            if acct_type == "BANK":
                msgsrsv1_open = "<BANKMSGSRSV1>"
                msgsrsv1_close = "</BANKMSGSRSV1>"
                acct_block = f"""
                <BANKACCTFROM>
                    <BANKID>021000021</BANKID>
                    <ACCTID>{acct_id}</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>"""
                stmttrnrs_open = "<STMTTRNRS>"
                stmttrnrs_close = "</STMTTRNRS>"
                stmtrs_open = "<STMTRS>"
                stmtrs_close = "</STMTRS>"
            else:
                msgsrsv1_open = "<CREDITCARDMSGSRSV1>"
                msgsrsv1_close = "</CREDITCARDMSGSRSV1>"
                acct_block = f"""
                <CCACCTFROM>
                    <ACCTID>{acct_id}</ACCTID>
                    <ACCTTYPE>CREDITLINE</ACCTTYPE>
                </CCACCTFROM>"""
                stmttrnrs_open = "<CCSTMTTRNRS>"
                stmttrnrs_close = "</CCSTMTTRNRS>"
                stmtrs_open = "<CCSTMTRS>"
                stmtrs_close = "</CCSTMTRS>"

            header = f"""OFXHEADER:100
DATA:OFXSGML
VERSION:102
SECURITY:NONE
ENCODING:USASCII
CHARSET:1252
COMPRESSION:NONE
OLDFILEUID:NONE
NEWFILEUID:NONE
<OFX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>{now}</DTSERVER>
            <LANGUAGE>ENG</LANGUAGE>
            <FI>
                <ORG>Chase Web Download</ORG>
                <FID>02430</FID>
            </FI>
            <INTU.BID>02430</INTU.BID>
        </SONRS>
    </SIGNONMSGSRSV1>
    {msgsrsv1_open}
        {stmttrnrs_open}
            <TRNUID>1001</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            {stmtrs_open}
                <CURDEF>USD"""

            header += acct_block
            header += f"""
                <BANKTRANLIST>
                    <DTSTART>{dtstart}</DTSTART>
                    <DTEND>{dtend}</DTEND>
"""

            stmttrns = []
            for idx, row in df.iterrows():
                trntype = "CREDIT" if row["Amount"] > 0 else "DEBIT"
                dtposted = pd.to_datetime(row["Date"]).strftime("%Y%m%d%H%M%S")
                amount = f"{row['Amount']:.2f}"
                fitid = f"{idx+1:06d}{timestamp_suffix}"
                name = str(row["Schedule C Category"])[:32]
                memo = str(row["Description"])[:255]

                stmttrns.append(f"""
                    <STMTTRN>
                        <TRNTYPE>{trntype}</TRNTYPE>
                        <DTPOSTED>{dtposted}</DTPOSTED>
                        <TRNAMT>{amount}</TRNAMT>
                        <FITID>{fitid}</FITID>
                        <NAME>{name}</NAME>
                        <MEMO>{memo}</MEMO>
                    </STMTTRN>""")

            footer = f"""
                </BANKTRANLIST>
                <LEDGERBAL>
                    <BALAMT>0.00</BALAMT>
                    <DTASOF>{now}</DTASOF>
                </LEDGERBAL>
            {stmtrs_close}
        {stmttrnrs_close}
    {msgsrsv1_close}
</OFX>"""

            qbo_content = header + "".join(stmttrns) + footer

            save_path = filedialog.asksaveasfilename(defaultextension=".qbo", filetypes=[("QBO files", "*.qbo")])
            if save_path:
                with open(save_path, "w", encoding="ascii", errors="ignore") as f:
                    f.write(qbo_content)
                messagebox.showinfo("Success", f"QBO file saved successfully at:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = QBOConverterApp(root)
    root.mainloop()
