// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Typography } from 'antd';
import './styles/App.css';
import FileUploader from './components/FileUploader';

const { Header, Content } = Layout;

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <Typography.Title level={2} style={{ color: 'white' }}>
            Sayl App
          </Typography.Title>
        </Header>
        <Content style={{ padding: '50px' }}>
          <div className="site-layout-content">
            <Routes>
              <Route path="/" element={<FileUploader />} />
              {/* Add more routes here as needed */}
            </Routes>
          </div>
        </Content>
      </Layout>
    </Router>
  );
}

export default App;
