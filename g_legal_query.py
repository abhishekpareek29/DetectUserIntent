import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from googlesearch import search

df = pd.read_csv('data/lexis.csv')
query = list(df['query'])
q_link = {}

for q in query:
    try:
        q = q.replace(u'\xa7', "section")
    except:
        pass
    for j in search(str(q), num=1, stop=1, pause=2):
        q_link[q] = j

i = 0
count = 0
result = []
for key, value in q_link.items():
    try:
        R = fuzz.ratio(key, value)
        legal_list = ['AL Rule', 'Alabama Rule', 'AK Rule', 'Alaska Rule', 'AS Rule', 'American Samoa Rule', 'AZ Rule', 'Arizona Rule', 'AR Rule', 'Arkansas Rule', 'CA Rule', 'California Rule', 'CO Rule', 'Colorado Rule', 'CT Rule', 'Connecticut Rule', 'DE Rule', 'Delaware Rule', 'DC Rule', 'District Of Columbia Rule', 'FM Rule', 'Federated States Of Micronesia Rule', 'FL Rule', 'Florida Rule', 'GA Rule', 'Georgia Rule', 'GU Rule', 'Guam Rule', 'HI Rule', 'Hawaii Rule', 'ID Rule', 'Idaho Rule', 'IL Rule', 'Illinois Rule', 'IN Rule', 'Indiana Rule', 'IA Rule', 'Iowa Rule', 'KS Rule', 'Kansas Rule', 'KY Rule', 'Kentucky Rule', 'LA Rule', 'Louisiana Rule', 'ME Rule', 'Maine Rule', 'MH Rule', 'Marshall Islands Rule', 'MD Rule', 'Maryland Rule', 'MA Rule', 'Massachusetts Rule', 'MI Rule', 'Michigan Rule', 'MN Rule', 'Minnesota Rule', 'MS Rule', 'Mississippi Rule', 'MO Rule', 'Missouri Rule', 'MT Rule', 'Montana Rule', 'NE Rule', 'Nebraska Rule', 'NV Rule', 'Nevada Rule', 'NH Rule', 'New Hampshire Rule', 'NJ Rule', 'New Jersey Rule', 'NM Rule', 'New Mexico Rule', 'NY Rule', 'New York Rule', 'NC Rule', 'North Carolina Rule', 'ND Rule', 'North Dakota Rule', 'MP Rule', 'Northern Mariana Islands Rule', 'OH Rule', 'Ohio Rule', 'OK Rule', 'Oklahoma Rule', 'OR Rule', 'Oregon Rule', 'PW Rule', 'Palau Rule', 'PA Rule', 'Pennsylvania Rule', 'PR Rule', 'Puerto Rico Rule', 'RI Rule', 'Rhode Island Rule', 'SC Rule', 'South Carolina Rule', 'SD Rule', 'South Dakota Rule', 'TN Rule', 'Tennessee Rule', 'TX Rule', 'Texas Rule', 'UT Rule', 'Utah Rule', 'VT Rule', 'Vermont Rule', 'VI Rule', 'Virgin Islands Rule', 'VA Rule', 'Virginia Rule', 'WA Rule', 'Washington Rule', 'WV Rule', 'West Virginia Rule', 'WI Rule', 'Wisconsin Rule', 'WY Rule', 'Wyoming Rule', 'Acquittal', 'Active judge', 'Administrative Office of the United States Courts (AO)', 'Admissible', 'Adversary proceeding', 'Affidavit', 'Affirmed', 'Alternate juror', 'Alternative dispute resolution (ADR)', 'Amicus curiae', 'Answer', 'Appeal', 'Appellant', 'Appellate', 'Appellee', 'Arraignment', 'Article III judge', 'Assets', 'Assume', 'Automatic stay', 'Bail', 'Bankruptcy', 'Bankruptcy administrator', 'Bankruptcy code', 'Bankruptcy court', 'Bankruptcy estate', 'Bankruptcy judge', 'Bankruptcy petition', 'Bankruptcy trustee', 'Bench trial', 'Brief', 'Burden of proof', 'Business bankruptcy', 'Capital offense', 'Case file', 'Case law', 'Caseload', 'Cause of action', 'Chambers', 'Chapter 11', 'Chapter 12', 'Chapter 13', 'Chapter 13 trustee', 'Chapter 15', 'Chapter 7', 'Chapter 7 trustee', 'Chapter 9', 'Chief judge', 'Claim', 'Class action', 'Clerk of court', 'Collateral', 'Common law', 'Community service', 'Complaint', 'Concurrent sentence', 'Confirmation', 'Consecutive sentence', 'Consumer bankruptcy', 'Consumer debts', 'Contingent claim', 'Contract', 'Conviction', 'Counsel', 'Count', 'Court', 'Court reporter', 'Credit counseling', 'Creditor', 'Damages', 'De facto', 'De jure', 'De novo', 'Debtor', "Debtor's plan", 'Declaratory judgment', 'Default judgment', 'Defendant', 'Defendant', 'Deposition', 'Discharge', 'Dischargeable debt', 'Disclosure statement', 'Discovery', 'Dismissal with prejudice', 'Dismissal without prejudice', 'Disposable income', 'Docket', 'Due process', 'En banc', 'Equitable', 'Equity', 'Evidence', 'Ex parte', 'Exclusionary rule', 'Exculpatory evidence', 'Executory contracts', 'Exempt assets', 'Exemptions, exempt property', 'Face sheet filing', 'Family farmer', 'Federal public defender', 'Federal public defender organization', 'Federal question jurisdiction', 'Felony', 'File', 'Fraudulent transfer', 'Fresh start', 'Grand jury', 'Habeas corpus', 'Hearsay', 'Home confinement', 'Impeachment', 'In camera', 'In forma pauperis', 'Inculpatory evidence', 'Indictment', 'Information', 'Injunction', 'Insider (of corporate debtor)', 'Insider (of individual debtor)', 'Interrogatories', 'Issue', 'Joint administration', 'Joint petition', 'Judge', 'Judgeship', 'Judgment', 'Judicial Conference of the United States', 'Jurisdiction', 'Jurisprudence', 'Jury', 'Jury instructions', 'Lawsuit', 'Lien', 'Liquidated claim', 'Liquidation', 'Litigation', 'Magistrate judge', 'Means test', 'Mental health treatment', 'Misdemeanor', 'Mistrial', 'Moot', 'Motion', 'Motion in Limine', 'Motion to lift the automatic stay', 'No-asset case', 'Nolo contendere', 'Nondischargeable debt', 'Nonexempt assets', 'Objection to dischargeability', 'Objection to exemptions', 'Opinion', 'Oral argument', 'Panel', 'Parole', 'Party in interest', 'Per curiam', 'Peremptory challenge', 'Petit jury (or trial jury)', 'Petition', 'Petition preparer', 'Petty offense', 'Plaintiff', 'Plan', 'Plea', 'Pleadings', 'Postpetition transfer', 'Prebankruptcy planning', 'Precedent', 'Preferential debt payment', 'Presentence report', 'Pretrial conference', 'Pretrial services', 'Priority', 'Priority claim', 'Pro per', 'Pro se', 'Pro tem', 'Probation', 'Probation officer', 'Procedure', 'Proof of claim', 'Property of the estate', 'Prosecute', 'Reaffirmation agreement', 'Record', 'Redemption', 'Remand', 'Reverse', 'Sanction', 'Schedules', 'Secured creditor', 'Secured debt', 'Senior judge', 'Sentence', 'Sentencing guidelines', 'Sequester', 'Service of process', 'Settlement', 'Small business case', 'Standard of proof', 'Statement of financial affairs', 'Statement of intention', 'Statute', 'Statute of limitations', 'Sua sponte', 'Subordination', 'Subpoena', 'Subpoena duces tecum', 'Temporary restraining order', 'Testimony', 'Toll', 'Tort', 'Transcript', 'Transfer', 'Trustee', 'Typing service', 'U.S. attorney', 'U.S. trustee', 'Undersecured claim', 'Undue hardship', 'Unlawful detainer action', 'Unliquidated claim', 'Unscheduled debt', 'Unsecured claim', 'Uphold', 'Venue', 'Verdict', 'Voir dire', 'Voluntary transfer', 'Wage garnishment', 'Warrant', 'Witness', 'Writ', 'Writ of certiorari']
        legal_val = False
        count = count + 1
        for legal_item in legal_list:
            if fuzz.ratio(legal_item, value) > 50:
                legal_val = True
        if R > 5 or legal_val is True:
            df.loc[i, 'google_fuzz_match'] = 1
            df.loc[i, 'google_fuzz_match_url'] = j
        else:
            df.loc[i, 'google_fuzz_match'] = 0
            df.loc[i, 'google_fuzz_match_url'] = j
        result.append(','.join([q, text_a, text_p]))
        if count % 100 == 0:
            with open("crnl.csv", "a") as f:
                for r in result:
                    f.write('\n' + r)
            result = []
        i += 1
    except:
        continue
