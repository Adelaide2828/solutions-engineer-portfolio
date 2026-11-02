"""
NumiKnow Agentic Verification Oracle - Execution Runner
Demonstrates deterministic evaluation of field claims against a policy manifest rubric.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Ensure stdout handles UTF-8 cleanly on Windows
if sys.platform.startswith("win"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def evaluate_claim(claim, manifest):
    """
    Evaluates a single claim against the rules defined in the manifest.
    Returns: verdict, details_list, payout_amount
    """
    verdict = "APPROVED"
    reasons = []
    payout = 0.0

    # Rule 1: Facilitator Certificate Score
    cert_rule = next(r for r in manifest['rules'] if r['id'] == 'R1')
    if claim['facilitatorCertScore'] < cert_rule['threshold']:
        return "REJECTED", [f"R1 Breach: Cert score {claim['facilitatorCertScore']} < {cert_rule['threshold']}"], 0.0

    # Rule 2: Geofence Validation
    geo_rule = next(r for r in manifest['rules'] if r['id'] == 'R2')
    if claim['gpsDistanceMeters'] > geo_rule['hardRejectThreshold']:
        return "REJECTED", [f"R2 Hard Breach: GPS distance {claim['gpsDistanceMeters']}m exceeds hard limit ({geo_rule['hardRejectThreshold']}m)"], 0.0
    elif claim['gpsDistanceMeters'] > geo_rule['threshold']:
        reasons.append(f"R2 Soft Anomaly: GPS distance {claim['gpsDistanceMeters']}m exceeds preferred limit ({geo_rule['threshold']}m)")
        verdict = "ESCALATED"

    # Rule 3: Evidence Screenshot Clarity
    img_rule = next(r for r in manifest['rules'] if r['id'] == 'R3')
    if claim['imageClarityConfidence'] < img_rule['threshold']:
        reasons.append(f"R3 Quality Anomaly: Image clarity confidence {claim['imageClarityConfidence']:.2f} < {img_rule['threshold']:.2f}")
        verdict = "ESCALATED"

    # Rule 4: Score Delta Outlier Check
    delta_rule = next(r for r in manifest['rules'] if r['id'] == 'R4')
    if claim['scoreDeltaPoints'] > delta_rule['threshold']:
        reasons.append(f"R4 Statistical Outlier: Score jump +{claim['scoreDeltaPoints']} pts exceeds max plausibility threshold ({delta_rule['threshold']})")
        verdict = "ESCALATED"

    # Rule 5: Roster Registration Check
    roster_rule = next(r for r in manifest['rules'] if r['id'] == 'R5')
    if not claim.get('isRegisteredLearner', True):
        reasons.append("R5 Identity Flag: Learner name/DID not found in enrolled school roster")
        verdict = "ESCALATED"

    if verdict == "APPROVED":
        payout = manifest.get('baseIncentivePerLearner', 15.0)
        reasons.append("All checks passed verified threshold")

    return verdict, reasons, payout

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, 'rubric_manifest.json')
    claims_path = os.path.join(script_dir, 'claims_dataset.json')

    if not os.path.exists(manifest_path) or not os.path.exists(claims_path):
        print(f"Error: Missing rubric_manifest.json or claims_dataset.json in {script_dir}")
        sys.exit(1)

    manifest = load_json(manifest_path)
    claims = load_json(claims_path)

    current_utc = datetime.now(timezone.utc).isoformat()

    print("=" * 72)
    print(" NUMIKNOW AGENTIC VERIFICATION ORACLE - EVALUATION PIPELINE")
    print(f" Policy Manifest: {manifest['manifestId']} (v{manifest['version']})")
    print(f" Target Domain:   {manifest['domainDid']}")
    print(f" Timestamp:       {current_utc}")
    print("=" * 72)
    print(f"\nProcessing {len(claims)} submitted field claims...\n")

    counts = {"APPROVED": 0, "REJECTED": 0, "ESCALATED": 0}
    total_disbursed = 0.0

    for idx, claim in enumerate(claims, 1):
        claim_id = claim['claimId']
        school = claim['schoolName']
        verdict, reasons, payout = evaluate_claim(claim, manifest)
        counts[verdict] += 1
        total_disbursed += payout

        status_symbols = {
            "APPROVED": "[PASS] APPROVED",
            "REJECTED": "[FAIL] REJECTED",
            "ESCALATED": "[WARN] ESCALATED TO HUMAN AUDITOR"
        }

        print(f"[{idx}/{len(claims)}] Claim: {claim_id} | School: {school}")
        print(f"      Outcome: {status_symbols[verdict]}")
        for r in reasons:
            print(f"      - {r}")
        if payout > 0:
            print(f"      - Incentive Scheduled: {payout:.2f} {manifest['currency']}")
        print()

    print("=" * 72)
    print(" ORACLE EXECUTION SUMMARY")
    print(f" Total Processed: {len(claims)}")
    print(f" Approved:        {counts['APPROVED']} ({counts['APPROVED']/len(claims)*100:.1f}%)")
    print(f" Rejected:        {counts['REJECTED']} ({counts['REJECTED']/len(claims)*100:.1f}%)")
    print(f" Escalated (HITL):{counts['ESCALATED']} ({counts['ESCALATED']/len(claims)*100:.1f}%)")
    print(f" Total Incentive: {total_disbursed:.2f} {manifest['currency']}")
    print("=" * 72)

if __name__ == '__main__':
    main()
