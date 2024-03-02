# The Cloud Resume Challenge

My first hands-on cloud project was
This wasn't my first attempt at hosting my own portfolio online. I'd completed at few HTML/CSS resume YT videos

The challenge consists of 16 total steps starting with becoming a certified AWS Cloud Practitioner, which I earned in 2023


* Deploy a HTML/CSS resume as a static website using Amazon S3 using a custom DNS domain name
* Securing the site with HTTPS
* Adding a visitor counter with Javascript, a DynamoDB database, API  calls and AWS Lambda backend
* Testing the code
* Deploy some Infrastructure as Code (IaC)
* Source Control, CI/CD front & back ends
* Write a blog post about the experience

https://docs.aws.amazon.com/AmazonS3/latest/userguide/website-hosting-custom-domain-walkthrough.html#root-domain-walkthrough-configure-redirect


## Frontend

Having built an HTML/CSS website and hosted via S3 previously, I breezed through Steps 2-4. After reading some AWS documentation and skimming a video, I jumped into the next step and struggled thought securing my site with HTTPS because I'd orginally created a single bucket instead of two. After a week of mostly error, reading documentation and watching more videos, I finally sat down one day after work, deleted everything from both buckets and started over. Twenty minutes and a [great walkthrough](https://www.youtube.com/watch?v=mls8tiiI3uc) later, I had a freshly secured static site using Route53, ACM and Amazon CloudFront services. 


## Backend 
Need to learn Terraform

## Testing

## IaC & CI/CD

## Thoughts
