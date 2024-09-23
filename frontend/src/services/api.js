// src/services/api.js
import axios from 'axios';
import FileDownload from 'js-file-download';
import { message } from 'antd';

const apiClient = axios.create({
  baseURL: 'https://backend.sayl.io/', // Base URL for your API
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  responseType: 'blob', // Handle binary data
});

const uploadFiles = async (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('pdfs', file); // Changed key from 'images' to 'pdfs'
  });

  try {
    const response = await apiClient.post('process-pdfs', formData);

    const contentDisposition = response.headers['content-disposition'];
    let filename = 'downloaded_file.pdf'; // Default filename

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1];
      }
    }

    FileDownload(response.data, filename);
    message.success('File downloaded successfully.');
  } catch (error) {
    console.error('Error uploading PDFs:', error);
    message.error('Error processing PDFs. Please try again.');
  }
};

const api = {
  uploadFiles,
};

export default api;
