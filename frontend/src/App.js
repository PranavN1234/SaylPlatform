// src/App.js
import React, { useState } from 'react';
import { Layout, Typography, Card, Button, Spin, message } from 'antd';
import DragAndDrop from './components/DragAndDrop';
import useFileSelection from './hooks/useFileSelection';
import './styles/App.css';
import axios from 'axios';
import FileDownload from 'js-file-download';

const { Header, Content } = Layout;

function App() {
  const [addFile, removeFile, selectedFiles] = useFileSelection();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (selectedFiles.length === 0) {
      message.error('Please upload at least one file.');
      return;
    }
  
    const formData = new FormData();
    selectedFiles.forEach((file) => {
      formData.append('images', file);
    });
  
    setLoading(true);
  
    try {
      const response = await axios.post(`http://ec2-34-230-86-87.compute-1.amazonaws.com/process-images`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob', // Important to handle binary data
      });
  
      // Check if content-disposition header is present
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
      console.error('Error uploading images:', error);
      message.error('Error processing images. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout className="layout">
      <Header>
        <Typography.Title level={2} style={{ color: 'white' }}>
          Sayl
        </Typography.Title>
      </Header>
      <Content style={{ padding: '50px' }}>
        <div className="site-layout-content">
          <Card
            style={{ margin: 'auto', width: '50%' }}
            actions={[
              <Button type="primary" onClick={handleSubmit} disabled={loading}>
                {loading ? <Spin /> : 'Submit'}
              </Button>,
            ]}
          >
            <DragAndDrop addFile={addFile} removeFile={removeFile} />
          </Card>
        </div>
      </Content>
    </Layout>
  );
}

export default App;
