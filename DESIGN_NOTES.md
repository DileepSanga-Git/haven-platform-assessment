# Design Notes

## B2 — idempotency key

State exactly what key your `cost_tag_check.py` uses to decide a plan has already been
checked/reported on. Use the word "idempotency" in your explanation.

The exact key used by cost_tag_check.py to identify and redepluicate reported resources is  in the terraform resource address, obtained from each entry in resource_changes.

for example:

aws_s3_bucket.listing_media
aws_lambda_function.mls_feed_sync

I used python set of resource addresses to prevent duplicate findings within a single execution. I sort the addresses before printing them to ensure output.

i'm checking it with stateless it does not store previously processed plans or modify the input plan. when the same unchnaged plan is checked again, it produces the same findings and exit status.

this provides idempotency across repeated executions without requring a database,or storage of plans.

The required billing page of tag key is landlord_account_id. This is separate from the resource address used as the idempotency and reporting key.

