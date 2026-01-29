# 🔥 URGENT: Open Port 8080 in EC2 Security Group

## Problem
Your application IS running on EC2, but port 8080 is blocked by AWS Security Group firewall.

## Verified Status
✅ Frontend server running: `http://localhost:8080` (works from inside EC2)
✅ Backend server running: `http://localhost:8000` (works from inside EC2)
❌ Port 8080 blocked from internet

## Solution: Open Port 8080

### Step-by-Step Instructions

1. **Go to AWS EC2 Console:**
   - https://ap-southeast-2.console.aws.amazon.com/ec2/

2. **Find Your Instance:**
   - Click "Instances" in left sidebar
   - Find instance with IP `13.211.53.117`
   - Click on it

3. **Go to Security Group:**
   - Scroll down to "Security" tab
   - Click on the Security Group name (looks like `sg-xxxxxxxxx`)

4. **Edit Inbound Rules:**
   - Click "Edit inbound rules" button
   - Click "Add rule"

5. **Add Rule for Port 8080:**
   - **Type:** Custom TCP
   - **Port range:** 8080
   - **Source:** Anywhere-IPv4 (0.0.0.0/0)
   - **Description:** AI Reviewer Frontend

6. **Add Rule for Port 8000 (if not already there):**
   - **Type:** Custom TCP
   - **Port range:** 8000
   - **Source:** Anywhere-IPv4 (0.0.0.0/0)
   - **Description:** AI Reviewer Backend

7. **Save Rules:**
   - Click "Save rules"
   - Wait 5 seconds

8. **Test:**
   - Visit http://13.211.53.117:8080
   - Should load the application!

## Alternative: Use Command Line (AWS CLI)

If you have AWS CLI configured:

```bash
# Find security group ID
aws ec2 describe-instances --filters "Name=ip-address,Values=13.211.53.117" --query "Reservations[0].Instances[0].SecurityGroups[0].GroupId" --output text

# Add port 8080 rule (replace sg-xxxxx with your security group ID)
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 8080 \
  --cidr 0.0.0.0/0

# Add port 8000 rule if needed
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0
```

## What Should Be Open

Your security group should allow:
- ✅ Port 22 (SSH) - Already open
- ✅ Port 80 (HTTP) - Optional  
- ✅ Port 8000 (Backend API) - **ADD THIS**
- ✅ Port 8080 (Frontend) - **ADD THIS**

## After Opening Ports

Test these URLs in your browser:
1. Frontend: http://13.211.53.117:8080
2. Backend API Docs: http://13.211.53.117:8000/docs
3. Backend Health: http://13.211.53.117:8000/health

---

## Confirmation Test

From your Windows machine, run:
```powershell
Test-NetConnection -ComputerName 13.211.53.117 -Port 8080
Test-NetConnection -ComputerName 13.211.53.117 -Port 8000
```

Should show: `TcpTestSucceeded : True`
