#!/usr/bin/env python3
"""Page Markdown headings and read bounded UTF-8 JSON with lossless cursors."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def encoded(value):
    return json.dumps(value,ensure_ascii=False).encode('utf-8')


def inventory(lines):
    sections=[]; fence=None; stack=[]
    for n,line in enumerate(lines,1):
        marker=re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$',line.rstrip('\r\n'))
        if marker:
            token,rest=marker.groups()
            if fence is None:
                if token[0]=='`' and '`' in rest: continue
                fence=token
            elif token[0]==fence[0] and len(token)>=len(fence) and not rest.strip(): fence=None
            continue
        if fence: continue
        heading=re.match(r'^ {0,3}(#{1,6})[ \t]+(.+?)\s*$',line)
        if heading:
            title=re.sub(r'[ \t]+#+[ \t]*$','',heading[2])
            level=len(heading[1])
            while stack and sections[stack[-1]]['level']>=level:
                sections[stack.pop()]['end']=n-1
            sections.append({'heading':title[:200],'heading_truncated':len(title)>200,
                             'level':level,'start':n,'end':len(lines)})
            stack.append(len(sections)-1)
    if not sections or sections[0]['start']>1:
        sections.insert(0,{'heading':'(preamble)' if sections else '(unstructured document)',
                          'heading_truncated':False,'level':0,'start':1,
                          'end':sections[0]['start']-1 if sections else len(lines)})
    return sections


def read_page(lines,start,column,max_lines,budget,base):
    if not lines:
        if start!=1 or column: raise ValueError('invalid cursor for empty document')
        return {**base,'start':1,'column':0,'end':0,'end_column':0,'content':'','next_start':None,'next_column':0}
    if start<1 or start>len(lines) or column<0 or column>=len(lines[start-1]):
        raise ValueError('cursor is outside document; no range was read')
    parts=[lines[start-1][column:],*lines[start:start+max_lines-1]]
    text=''.join(parts)
    def output(count):
        remaining=count;line=start;col=column;end=start;end_col=column
        while remaining:
            available=len(lines[line-1])-col
            consumed=min(remaining,available)
            remaining-=consumed;col+=consumed;end=line;end_col=col
            if col==len(lines[line-1]): line+=1;col=0
        return {**base,'start':start,'column':column,'end':end,'end_column':end_col,
                'content':text[:count],'next_start':line if line<=len(lines) else None,'next_column':col}
    # Budget includes serialized metadata, escapes and multibyte Unicode, so
    # an 8KB page stays under a 10KB tool cap even for a quote/emoji-heavy line.
    low,high=0,len(text)
    while low<high:
        middle=(low+high+1)//2
        if len(encoded(output(middle)))<=budget: low=middle
        else: high=middle-1
    if low==0: raise ValueError('page budget too small for metadata and one character')
    return output(low)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='mode',required=True)
    for mode in ('index','read'):
        command=sub.add_parser(mode)
        command.add_argument('path')
        command.add_argument('--max-chars',type=int,default=8000,help='Serialized UTF-8 page budget, including metadata (max 8000).')
        command.add_argument('--expected-sha',help='Fail if the document changed since its heading inventory.')
        if mode=='index':
            command.add_argument('--offset',type=int,default=0)
            command.add_argument('--limit',type=int,default=30)
        else:
            command.add_argument('--start',type=int,default=1)
            command.add_argument('--column',type=int,default=0,help='Character offset within the start line, from prior cursor.')
            command.add_argument('--max-lines',type=int,default=120)
    args=parser.parse_args()
    try:
        if not 512<=args.max_chars<=8000: raise ValueError('--max-chars must be between 512 and 8000')
        data=Path(args.path).read_bytes();sha=hashlib.sha256(data).hexdigest()
        if args.expected_sha and args.expected_sha!=sha: raise ValueError('document changed; rebuild inventory and review coverage')
        lines=data.decode('utf-8').splitlines(keepends=True)
        base={'path':args.path,'sha256':sha,'total_lines':len(lines)}
        if args.mode=='index':
            if args.limit<1 or args.offset<0: raise ValueError('index offset/limit is invalid')
            sections=inventory(lines)
            if args.offset>len(sections): raise ValueError('index offset is outside heading inventory')
            page=[]
            for item in sections[args.offset:args.offset+args.limit]:
                candidate={**base,'sections':page+[item],'total_sections':len(sections),
                           'next_offset':args.offset+len(page)+1 if args.offset+len(page)+1<len(sections) else None}
                if len(encoded(candidate))>args.max_chars: break
                page.append(item)
            if args.offset<len(sections) and not page: raise ValueError('page budget too small for one heading')
            output={**base,'sections':page,'total_sections':len(sections),
                    'next_offset':args.offset+len(page) if args.offset+len(page)<len(sections) else None}
        else:
            if args.max_lines<1: raise ValueError('--max-lines must be positive')
            output=read_page(lines,args.start,args.column,args.max_lines,args.max_chars,base)
        sys.stdout.buffer.write(encoded(output)+b'\n')
    except (OSError,ValueError,UnicodeError) as error:
        print(f'NOT ASSESSED: document read failed: {error}',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':sys.exit(main())
