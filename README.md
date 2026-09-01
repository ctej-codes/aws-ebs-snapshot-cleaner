# AWS EBS Snapshot Cleaner

A Python automation script that identifies and deletes orphaned AWS EBS snapshots to help reduce storage costs and maintain cloud resource hygiene.

## Overview

Amazon EBS snapshots are commonly used for backups and disaster recovery. Over time, as EC2 instances and EBS volumes are deleted, associated snapshots may remain in the AWS account and continue to consume storage.

This script automates the process of identifying and removing snapshots that are no longer associated with valid or actively attached EBS volumes.

## Features

- Retrieves all EBS snapshots owned by the AWS account.
- Verifies whether the source EBS volume exists.
- Checks whether the volume is attached to any EC2 instance.
- Deletes snapshots whose volumes:
  - No longer exist.
  - Exist but are not attached to any instance.
  - Do not have an associated volume ID.
- Handles AWS API exceptions gracefully.

## How It Works

### Step 1: Retrieve EC2 Instances

The script fetches all EC2 instances that are currently in either:

- Running state
- Stopped state

### Step 2: Retrieve EBS Snapshots

The script retrieves all EBS snapshots owned by the AWS account.

### Step 3: Validate Snapshot Volume

For each snapshot, the script:

1. Checks whether the snapshot contains a valid Volume ID.
2. Verifies that the volume still exists.
3. Checks whether the volume is attached to an EC2 instance.

### Step 4: Delete Orphaned Snapshots

The snapshot is deleted if:

- The associated volume does not exist.
- The volume exists but is not attached to any EC2 instance.
- The snapshot has no associated Volume ID.

## Architecture Flow

```text
EBS Snapshots
      |
      v
Check Volume ID
      |
  +---+---+
  |       |
Missing  Exists
  |       |
Delete    v
       Check Volume
           |
      +----+----+
      |         |
   Missing   Exists
      |         |
   Delete      v
         Check Attachments
                |
           +----+----+
           |         |
      Attached   Not Attached
           |         |
          Keep    Delete
```

## Prerequisites

- Python 3.x
- AWS Account
- AWS CLI configured
- Appropriate IAM permissions

## Required Permissions

The IAM user or role executing the script should have the following permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeVolumes",
        "ec2:DescribeSnapshots",
        "ec2:DeleteSnapshot"
      ],
      "Resource": "*"
    }
  ]
}
```

## Installation

Clone the repository:

```bash
git clone https://github.com/ctej-codes/aws-ebs-snapshot-cleaner.git

cd aws-ebs-snapshot-cleaner
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

Create a `requirements.txt` file:

```text
boto3
botocore
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python src/snapshot_cleaner.py
```

## Example Output

```text
Deleted the snap-0123456789abcdef as the volume is not associated with the snapshot

Deleted the snap-0987654321abcdef as the volume is not attached to any instance

Deleted the snap-0abc123def456789 as the volume is not found
```

## Use Cases

### Cost Optimization

Remove unused snapshots that continue consuming storage and increasing AWS costs.

### Cloud Resource Cleanup

Maintain a clean AWS environment by automatically removing stale resources.

### Governance and Compliance

Regularly review and clean backup artifacts that are no longer required.

### DevOps Automation

Integrate the script into scheduled jobs, CI/CD pipelines, or maintenance workflows.

## Limitations

- The script permanently deletes snapshots.
- No dry-run mode is currently implemented.
- No age-based filtering is applied.
- No tag-based exclusions are configured.

## Learning Outcomes

This project demonstrates:

- AWS EC2 and EBS resource management
- Boto3 SDK usage
- AWS automation with Python
- Exception handling for AWS APIs
- Infrastructure cost optimization
- Cloud governance best practice

## Author

**Charan Tej**

Python | AWS | Cloud Automation | DevOps
