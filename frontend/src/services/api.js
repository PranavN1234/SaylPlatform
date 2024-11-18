// src/services/api.js
import axios from 'axios';
import FileDownload from 'js-file-download';
import { message } from 'antd';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/', // Base URL for your API
  headers: {
    'Content-Type': 'multipart/form-data',
  },
  responseType: 'blob', // Handle binary data
});

const uploadFiles = async (files) => {
  const formData = new FormData();
  files.forEach((file) => {
    formData.append('pdfs', file); // Key matches backend
  });

  try {
    const response = await apiClient.post('process-BOL-pdfs', formData);

    const contentDisposition = response.headers['content-disposition'];
    let filename = 'filled_forms.zip'; // Default filename

    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?([^"]+)"?/);
      if (filenameMatch && filenameMatch[1]) {
        filename = filenameMatch[1];
      }
    }

    // Use FileDownload to save the ZIP file
    FileDownload(response.data, filename);
    message.success('Forms downloaded successfully.');
  } catch (error) {
    console.error('Error uploading PDFs:', error);
    message.error('Error processing PDFs. Please try again.');
  }
};

const api = {
  uploadFiles,
};

export default api;