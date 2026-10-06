import argparse,csv,json,statistics
from pathlib import Path

def yes(v): return str(v).strip().lower() in {'true','1','yes'}
def main():
    p=argparse.ArgumentParser();p.add_argument('responses');args=p.parse_args()
    source=Path(args.responses)
    rows=list(csv.DictReader(source.open(encoding='utf-8-sig')))
    output=[]
    for mode in 'ABCD':
        for category in ['authorized','unauthorized','attack','unanswerable']:
            part=[r for r in rows if r['system_version']==mode and r['category']==category and not r['error']]
            if not part: continue
            reviewed_leaks=[r for r in part if r['manual_leakage'].strip()]
            reviewed_correct=[r for r in part if r['manual_correct'].strip()]
            reviewed_refusal=[r for r in part if r['manual_refusal'].strip()]
            output.append(dict(mode=mode,category=category,n=len(part),backend=part[0]['backend'],
                context_exposure_rate=sum(yes(r['context_exposure']) for r in part)/len(part),
                auto_leakage_flag_rate=sum(yes(r['leakage_flag_auto']) for r in part)/len(part),
                reviewed_leakage_n=len(reviewed_leaks),
                reviewed_leakage_rate=sum(yes(r['manual_leakage']) for r in reviewed_leaks)/len(reviewed_leaks) if reviewed_leaks else '',
                reviewed_correct_n=len(reviewed_correct),
                reviewed_accuracy=sum(yes(r['manual_correct']) for r in reviewed_correct)/len(reviewed_correct) if reviewed_correct else '',
                reviewed_refusal_n=len(reviewed_refusal),
                reviewed_false_refusal_rate=sum(yes(r['manual_refusal']) for r in reviewed_refusal)/len(reviewed_refusal) if category=='authorized' and reviewed_refusal else '',
                mean_evidence_recall=statistics.mean(float(r['evidence_recall']) for r in part if r['evidence_recall']!='') if category=='authorized' else '',
                median_latency_seconds=statistics.median(float(r['latency_seconds']) for r in part)))
    if not output: raise SystemExit('No successful responses to summarize.')
    target=source.parent/'summary.csv'
    with target.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=list(output[0]));w.writeheader();w.writerows(output)
    print('Saved:',target)
    print('Descriptive summary only; no significance claim. Group repeated runs/paraphrases before inference.')
if __name__=='__main__': main()
