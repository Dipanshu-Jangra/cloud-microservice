# AWS Setup (one-time)

Do these steps once. After that, every push to `main` deploys automatically.

## 1. Create an ECR repository
1. AWS Console → search **ECR** → **Create repository**.
2. Visibility: **Private**. Name: `cloud-microservice`. Create.

## 2. Create an IAM user for GitHub Actions
1. Console → **IAM → Users → Create user** (name: `github-actions`).
2. Attach policy **AmazonEC2ContainerRegistryPowerUser**.
3. Open the user → **Security credentials → Create access key** (use case: *Third-party service*).
4. Save the **Access key ID** and **Secret access key**.

## 3. Create an IAM role for the EC2 instance (so it can pull from ECR)
1. **IAM → Roles → Create role** → trusted entity: **AWS service → EC2**.
2. Attach **AmazonEC2ContainerRegistryReadOnly**. Name it `ec2-ecr-read`.

## 4. Launch the EC2 instance
1. **EC2 → Launch instance**. Name: `cloud-microservice`.
2. AMI: **Amazon Linux 2023**. Type: **t2.micro / t3.micro** (free tier).
3. Key pair: **Create new key pair** (RSA, `.pem`). Keep the downloaded file safe.
4. Network settings → security group, allow inbound:
   - **SSH (22)** from Anywhere (needed so GitHub Actions can connect)
   - **HTTP (80)** from Anywhere (0.0.0.0/0)
5. Advanced details → **IAM instance profile** → `ec2-ecr-read`.
6. Launch.

## 5. Install Docker on the instance
Connect (EC2 console → **Connect → EC2 Instance Connect**), then run:
```bash
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker ec2-user
exit
```
(Reconnect once so the group change applies.)

## 6. Add GitHub repository secrets
GitHub repo → **Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | from step 2 |
| `AWS_SECRET_ACCESS_KEY` | from step 2 |
| `AWS_REGION` | e.g. `ap-south-1` (the region you created ECR/EC2 in) |
| `ECR_REPOSITORY` | `cloud-microservice` |
| `EC2_HOST` | EC2 public IPv4 address |
| `EC2_USER` | `ec2-user` |
| `EC2_SSH_KEY` | full contents of the `.pem` file |

## 7. Block merges when tests fail
GitHub repo → **Settings → Branches → Add branch protection rule**:
- Branch name pattern: `main`
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging → select **test**
- Save.

Now work on a branch, open a pull request, and GitHub will refuse to merge if tests fail.

## 8. Clean up (avoid charges)
When finished with the assessment: stop/terminate the EC2 instance and delete the ECR repository.
