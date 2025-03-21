# Image Processing System

## Overview

This system processes image data from CSV files asynchronously. It accepts a CSV file containing product names and input image URLs, validates the data, compresses the images by 50% of their original quality, stores the processed images, and provides APIs to track the processing status.

## Features

- **CSV Upload & Validation:** Accepts CSV files with a predefined format and validates their content.
- **Asynchronous Image Processing:** Compresses images without blocking execution.
- **Storage:** Saves processed images and product information in a database.
- **Status Tracking:** Provides a unique request ID to track processing progress.
- **Webhook Support:** Notifies a specified endpoint when processing is complete.
- **API Endpoints:**
  - Upload API
  - Status API

## Input CSV Format

The system expects a CSV file with the following format:

| S. No. | Product Name | Input Image URLs                                                                   |
| ------ | ------------ | ---------------------------------------------------------------------------------- |
| 1      | SKU1         | [https://image1.jpg](https://image1.jpg), [https://image2.jpg](https://image2.jpg) |
| 2      | SKU2         | [https://image3.jpg](https://image3.jpg), [https://image4.jpg](https://image4.jpg) |

## Output CSV Format

After processing, an output CSV file will be generated with compressed image URLs added:

| S. No. | Product Name | Input Image URLs                                                                   | Output Image URLs                                                                      |
| ------ | ------------ | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1      | SKU1         | [https://image1.jpg](https://image1.jpg), [https://image2.jpg](https://image2.jpg) | [https://output1.jpg](https://output1.jpg), [https://output2.jpg](https://output2.jpg) |
| 2      | SKU2         | [https://image3.jpg](https://image3.jpg), [https://image4.jpg](https://image4.jpg) | [https://output3.jpg](https://output3.jpg), [https://output4.jpg](https://output4.jpg) |

## API Endpoints

### 1. Upload API

- **Endpoint:** `/upload`
- **Method:** `POST`
- **Description:** Accepts a CSV file, validates it, and returns a unique request ID.
- **Response:** `{ "request_id": "abc123" }`

### 2. Status API

- **Endpoint:** `/status/{request_id}`
- **Method:** `GET`
- **Description:** Returns the processing status for a given request ID.
- **Response:** `{ "status": "processing" | "completed" }`

### 3. Webhook Integration&#x20;

- **Trigger:** When image processing is complete.

## System Architecture

The system consists of:

1. **Image Processing Service:** Handles asynchronous image compression.
2. **Database:** Stores product details and processing status.
3. **Worker Queue:** Manages asynchronous tasks.
4. **API Gateway:** Exposes REST endpoints for interaction.
5. **Webhook Handler:** Notifies external services upon completion.

## Database Schema

- **Products Table:** Stores product details and input/output image URLs.
- **Processing Requests Table:** Tracks the status of each CSV file request.

## API Documentation

Refer to the Postman collection for detailed API specifications.
