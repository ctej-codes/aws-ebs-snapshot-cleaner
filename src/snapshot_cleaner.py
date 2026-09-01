import boto3
from botocore.errorfactory import ClientError

# Create an EC2 client to interact with AWS EC2 and EBS resources
ec2 = boto3.client('ec2')


def main():
    """
    Identifies and removes orphaned EBS snapshots.

    A snapshot is considered orphaned if:
    1. It has no associated Volume ID.
    2. The associated volume no longer exists.
    3. The volume exists but is not attached to any EC2 instance.
    """

    # Retrieve all EC2 instances that are currently running or stopped.
    # Other states (terminated, shutting-down, etc.) are ignored.
    ec2_instances = ec2.describe_instances(
        Filters=[
            {
                'Name': 'instance-state-name',
                'Values': ['stopped', 'running']
            }
        ]
    )

    # Store active EC2 instance IDs for reference.
    # Using a set provides faster lookups if needed in future enhancements.
    ec2_instances_available = set()

    # Extract and store instance IDs from the response.
    for reservation in ec2_instances['Reservations']:
        for instance in reservation['Instances']:
            ec2_instances_available.add(instance['InstanceId'])

    # Retrieve all EBS snapshots owned by the current AWS account.
    ebs_snapshots_response = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    # Iterate through each snapshot for validation.
    for snap_shot in ebs_snapshots_response['Snapshots']:

        snapshot_id = snap_shot['SnapshotId']
        volume_id = snap_shot.get('VolumeId')

        # Scenario 1:
        # Snapshot does not have an associated volume.
        # Such snapshots are considered orphaned and can be deleted.
        if not volume_id:
            ec2.delete_snapshot(SnapshotId=snapshot_id)
            print(
                f"Deleted {snapshot_id} because no Volume ID is associated with the snapshot."
            )

        else:
            try:
                # Retrieve details of the source EBS volume.
                ec2_volumes_response = ec2.describe_volumes(
                    VolumeIds=[volume_id]
                )

                # Scenario 2:
                # Volume exists but is not attached to any EC2 instance.
                # Snapshots created from unused volumes can be cleaned up.
                if not ec2_volumes_response['Volumes'][0]['Attachments']:
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(
                        f"Deleted {snapshot_id} because the volume ({volume_id}) is not attached to any instance."
                    )

            except ClientError as e:

                # Scenario 3:
                # The source volume no longer exists in AWS.
                # Snapshot is considered orphaned and removed.
                if e.response["Error"]["Code"] == "InvalidVolume.NotFound":
                    ec2.delete_snapshot(SnapshotId=snapshot_id)
                    print(
                        f"Deleted {snapshot_id} because the source volume ({volume_id}) was not found."
                    )

                # Re-raise any unexpected AWS API exceptions.
                else:
                    raise


if __name__ == "__main__":
    main()
