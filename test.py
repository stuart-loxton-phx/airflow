import re
import hashlib

MAX_LABEL_LEN = 63


def make_safe_label_value(string, max_length=MAX_LABEL_LEN):
    """
    Valid label values must be 63 characters or less and must be empty or begin and
    end with an alphanumeric character ([a-z0-9A-Z]) with dashes (-), underscores (_),
    dots (.), and alphanumerics between.

    If the label value is greater than 63 chars once made safe, or differs in any
    way from the original value sent to this function, then we need to truncate to
    53 chars, and append it with a unique hash.
    """
    safe_label = re.sub(r"^[^a-z0-9A-Z]*|[^a-zA-Z0-9_\-\.]|[^a-z0-9A-Z]*$", "", string)

    if len(safe_label) > max_length or string != safe_label:
        safe_hash = hashlib.md5(string.encode()).hexdigest()[:9]
        safe_label = safe_label[:max_length - len(safe_hash) - 1] + "-" + safe_hash

    return safe_label


if __name__ == "__main__":
    label = make_safe_label_value("datainfra-primary-etl-validate-sink-offsets.c547fd62d011467f96a14b114fe79362")
    label = re.sub(r'[^a-z0-9.-]+', '-', "datainfra-primary-etl-validate-sink-offsets. c547fd62d011467f96a14b114fe79362")
    print(label)
