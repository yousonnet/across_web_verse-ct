1.once tweet was quoted (whatever delete or save),the status of quoted tweet will change to "is_quote_status:True"

2. repost type 's full_text start with RT @
3. reply chain 's full_text start with @
4. if is_quote_status:True and NOT start with RT @,that's quote

5.repost will not created a new conversation,quote will.

6.every reply definitely has it's own main conversation above

7.in_reply_status_id_str is replied message's id_str

8.once find main tweet ,inference step can be done.

9.if reply chain exceeds 3,twitter will fold the middle message,so only conversation_id_str can be same,reply_id doesn't make sense

10.may be from raw to text directly?
