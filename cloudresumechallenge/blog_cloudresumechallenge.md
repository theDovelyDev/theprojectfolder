# The Cloud Resume Challenge

My first hands-on cloud project was

As a FinOps professional, hands on experience designing and building in the cloud benefits my conversations with Engineering and Product teams. For those not familiar with the term, FinOps is basically the intersection of Finance and DevOps to maximize the business value of the cloud. Check out the [FinOps Foundation](https://www.finops.org/framework/) to learn more about the framework.

This wasn't my first attempt at hosting my own portfolio online. I've completed a few follow along HTML/CSS resume YT videos. Thanks to the hours I spent customizing my MySpace page (hello 2004 through 2007)

The challenge consists of 16 total steps starting with becoming a certified AWS Cloud Practitioner, which I earned in 2023. After earning the AWS CCP, I immediately jumped into studying for the Solutions Architect cert. 


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
Knowing zero Javascript, I approached the next steps out of order, first starting with creating my DynamoDB table, using a Lambda functional URL for my API, then finally Javascript. As a trained Data Analyst, who thought she wanted to be a DBA one day, setting up the DynamoDB table was a breeze.

Because I selected for Lambda to create a new role for calling the function, my inital functions failed due to explicit permission denial. After a quick trip over to the IAM console to update the role permissions and allow the newly created role to read and write to my DynamoDB table. Finally, I set the CORS orgin as the URL for my site making my Lambda function complete. 

![Lambda Functional URL architecture!](/cloudresumechallenge/frontend/images/



Need to learn Terraform

## Testing

## IaC & CI/CD

## Thoughts

If you decide to complete the challenge, I've created a YouTube playlist of all the videos I found helpful.