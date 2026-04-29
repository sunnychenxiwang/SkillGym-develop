Using all three provided files, create a single Excel workbook that quantifies and compares **FTP command behavior** in the two PCAPs and ties it back to the Wireshark Wiki “SampleCaptures” page as the reference source for these sample traces.

1) Parse `/root/ftp.pcap` and `/root/bruteforce.pcap` and reconstruct the FTP **control-channel** dialogue (TCP port 21) by extracting ASCII FTP commands sent from client to server (e.g., `USER`, `PASS`, `SYST`, `FEAT`, `CWD`, `PWD`, `TYPE`, `SIZE`, `PASV`, `RETR`, `QUIT`). Ignore server responses and ignore the passive-mode data connection (non-21 ports).

2) For each PCAP, compute a deterministic “command frequency table”:
- rows = FTP command verb (uppercase, no arguments)
- columns = `count` (number of times that verb appears in client→server commands on port 21)
- include only verbs that appear at least once in that PCAP

3) Use `/root/samplecaptures` (HTML) to extract the **page title** text (the `<title>` content) and write it into the Excel workbook as the provenance string in a cell labeled `Reference Page Title`.

4) Save a single Excel file to **exactly**:
`/root/ftp_command_comparison.xlsx`

Workbook requirements (must be satisfied exactly):
- Sheet `Summary`:
  - Cell A1: `Reference Page Title`
  - Cell B1: the extracted HTML `<title>` text from `samplecaptures`
  - A3:D3 header row with: `pcap`, `total_commands`, `unique_verbs`, `top_verb`
  - Row 4 summarizes `ftp.pcap`; Row 5 summarizes `bruteforce.pcap`
    - `total_commands` = total number of extracted client commands on port 21
    - `unique_verbs` = number of distinct verbs in that PCAP
    - `top_verb` = the single verb with the highest count (break ties by alphabetical order)
- Sheet `ftp_pcap`:
  - The command frequency table for `ftp.pcap`, sorted by `count` descending then verb ascending
- Sheet `bruteforce_pcap`:
  - The command frequency table for `bruteforce.pcap`, sorted by `count` descending then verb ascending

The task is complete only when the Excel file exists at the specified path and all computed values are derived solely from the three input files as described.