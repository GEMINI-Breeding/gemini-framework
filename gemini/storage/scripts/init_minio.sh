
# !/bin/bash
set -e

# Print environment variables
echo "Environment Variables:"
echo "MINIO_SERVER_HOST: ${MINIO_SERVER_HOST}"
echo "MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY}"
echo "MINIO_SECRET_KEY: ${MINIO_SECRET_KEY}"
echo "GEMINI_STORAGE_ACCESS_KEY: ${GEMINI_STORAGE_ACCESS_KEY}"
echo "GEMINI_STORAGE_SECRET_KEY: ${GEMINI_STORAGE_SECRET_KEY}"
echo "GEMINI_STORAGE_BUCKET_NAME: ${GEMINI_STORAGE_BUCKET_NAME}"

# Get environment variables
echo "Connect to MinIO server..."
mc alias set local http://${MINIO_SERVER_HOST}:9000 "${MINIO_ACCESS_KEY}" "${MINIO_SECRET_KEY}"

# Create a service account
echo "Creating service account..."
mc admin user add local "${GEMINI_STORAGE_ACCESS_KEY}" "${GEMINI_STORAGE_SECRET_KEY}"

# Create a policy file
echo "Creating policy file..."
POLICY_FILE="/tmp/policy.json"
cat << EOF > "${POLICY_FILE}"
{
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Action": [
            "s3:CreateBucket",
            "s3:DeleteBucket",
            "s3:GetObject",
            "s3:DeleteObject",
            "s3:PutObject",
            "s3:ListBucket",
            "s3:List*",
            "s3:GetBucketLocation"
        ],
        "Resource": [
            "arn:aws:s3:::${GEMINI_STORAGE_BUCKET_NAME}",
            "arn:aws:s3:::${GEMINI_STORAGE_BUCKET_NAME}/*"
        ]
    }]
}
EOF

# Add policy with verbose output
echo "Adding policy..."
mc admin policy create local gemini-service-policy "${POLICY_FILE}" --debug

# Show policy
echo "Showing policy info..."
mc admin policy info local gemini-service-policy

# Clean up temporary policy file
rm -f "${POLICY_FILE}"

# Assign policy to service account
echo "Assigning policy to service account..."
mc admin policy attach local gemini-service-policy --user "${GEMINI_STORAGE_ACCESS_KEY}"

# Create bucket if it doesn't exist
echo "Creating bucket..."
mc mb local/"${GEMINI_STORAGE_BUCKET_NAME}"

# Set bucket to private
echo "Setting bucket to private..."
mc policy set download local/"${GEMINI_STORAGE_BUCKET_NAME}"

echo "MinIO initialization completed successfully"







# Verify credentials
# echo "Verifying credentials..."
# mc admin info local

# GEMINI_STORAGE_HOSTNAME=gemini-storage
# GEMINI_STORAGE_PORT=9000
# GEMINI_STORAGE_API_PORT=9001
# GEMINI_STORAGE_ROOT_USER=gemini_root
# GEMINI_STORAGE_ROOT_PASSWORD=gemini_root
# GEMINI_STORAGE_ACCESS_KEY=gemini_storage_user
# GEMINI_STORAGE_SECRET_KEY=gemini_secret
# GEMINI_STORAGE_BUCKET_NAME=gemini

# Print environment variables
# echo "Environment Variables:"
# echo "GEMINI_STORAGE_BUCKET_NAME: ${GEMINI_STORAGE_BUCKET_NAME}"
# echo "GEMINI_STORAGE_ACCESS_KEY: ${GEMINI_STORAGE_ACCESS_KEY}"
# echo "GEMINI_STORAGE_SECRET_KEY: ${GEMINI_STORAGE_SECRET_KEY}"
# echo "MINIO_ROOT_USER: ${MINIO_ROOT_USER}"
# echo "MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}"
# echo "MINIO_ACCESS_KEY: ${MINIO_ACCESS_KEY}"
# echo "MINIO_SECRET_KEY: ${MINIO_SECRET_KEY}"



# # Start MinIO server
# echo "Starting MinIO server..."
# minio server /bitnami/minio/data --address :9000 --console-address ":9001" &

# until mc admin info local >/dev/null 2>&1; do
#     echo "Waiting for MinIO to be ready..."
#     sleep 1
# done

# echo "MinIO server is ready!"

# # Check required environment variables
# if [ -z "${GEMINI_STORAGE_BUCKET_NAME}" ] || [ -z "${GEMINI_STORAGE_ACCESS_KEY}" ] || [ -z "${GEMINI_STORAGE_SECRET_KEY}" ]; then
#     echo "Error: Required environment variables are not set"
#     exit 1
# fi



# # Verify credentials
# echo "Verifying credentials..."
# mc admin info local

# # Create service account user
# echo "Creating service account user..."
# mc admin user add local "${GEMINI_STORAGE_ACCESS_KEY}" "${GEMINI_STORAGE_SECRET_KEY}"


# # Create service account policy
# echo "Creating service account policy..."

# # Create temporary policy file
# POLICY_FILE="/tmp/policy.json"
# cat << EOF > "${POLICY_FILE}"
# {
#     "Version": "2012-10-17",
#     "Statement": [{
#         "Effect": "Allow",
#         "Action": [
#             "s3:CreateBucket",
#             "s3:DeleteBucket",
#             "s3:GetObject",
#             "s3:DeleteObject",
#             "s3:PutObject"
#         ],
#         "Resource": [
#             "arn:aws:s3:::${GEMINI_STORAGE_BUCKET_NAME}",
#             "arn:aws:s3:::${GEMINI_STORAGE_BUCKET_NAME}/*"
#         ]
#     }]
# }
# EOF

# if [ ! -f "${POLICY_FILE}" ]; then
#     echo "Error: Policy file not found: ${POLICY_FILE}"
#     exit 1
# fi

# # Add policy with verbose output
# echo "Adding policy..."
# mc admin policy create local gemini-service-policy "${POLICY_FILE}" --debug

# # Show policy
# echo "Showing policy info..."
# mc admin policy info local gemini-service-policy

# # Clean up temporary policy file
# rm -f "${POLICY_FILE}"


# # Assign policy to service account
# echo "Assigning policy to service account..."
# mc admin policy set local gemini-service-policy user="${GEMINI_STORAGE_ACCESS_KEY}"

# # Create bucket if it doesn't exist
# echo "Creating bucket..."
# mc mb local/"${GEMINI_STORAGE_BUCKET_NAME}"

# # Set bucket to private
# echo "Setting bucket to private..."
# mc policy set download local/"${GEMINI_STORAGE_BUCKET_NAME}"

# echo "MinIO initialization completed successfully"

