Create a single Excel workbook that **quantitatively compares brute-force vs. normal FTP behavior** using both PCAPs, and uses the Wireshark “SampleCaptures” HTML page to **label the protocol category** used for the analysis.

Using `/root/bruteforce.pcap` and `/root/ftp.pcap`, parse the FTP control-channel traffic (TCP/21) and compute, for each PCAP:

1. **server_ip** and **client_ip** (the two endpoints that carry the FTP control session(s), oriented so server_ip is the host that sends the `220` banner).
2. **total_login_attempts** = count of `PASS` commands observed on the control channel.
3. **unique_usernames** = number of distinct `USER <name>` values.
4. **most_targeted_username** = the username with the highest count of `USER` commands (break ties by lexicographic order).
5. **top_password_candidate** = the most frequent `PASS <value>` payload (break ties by lexicographic order).
6. **success_count** = number of successful logins, defined as a server response code `230` occurring after a `USER`/`PASS` sequence within the same TCP stream.
7. **bruteforce_score** = `total_login_attempts / max(1, unique_usernames)` (as a numeric value with 4 decimal places).

Then, using `/root/samplecaptures` (the Wireshark SampleCaptures HTML), extract the **protocol category label** for FTP as it appears as a section/category name in that page (use the exact visible heading text from the HTML that corresponds to FTP). Include this label in the workbook as `protocol_category`.

Deliverable requirements:

- Save an Excel file to **`/root/ftp_bruteforce_comparison.xlsx`**.
- The workbook must contain exactly **two sheets**:
  1. **`comparison`**: a table with one row per PCAP (`bruteforce.pcap`, `ftp.pcap`) and columns exactly named:  
     `pcap`, `protocol_category`, `server_ip`, `client_ip`, `total_login_attempts`, `unique_usernames`, `most_targeted_username`, `top_password_candidate`, `success_count`, `bruteforce_score`
  2. **`methods`**: a short, plain-text description (no more than 8 lines) of the deterministic rules you used to (a) identify server vs client, (b) count attempts, and (c) define success.
- Use Excel formatting conventions: header row bold; numeric columns right-aligned; `bruteforce_score` displayed with 4 decimal places.
- Do not output results to stdout as the final answer; **writing the Excel file is mandatory**.