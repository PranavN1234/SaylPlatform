// src/components/FileTile.js
import React from 'react';
import { Card, Button } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import PropTypes from 'prop-types';
import '../styles/FileTile.css'; // Ensure the CSS is imported

const FileTile = ({ file, onRemove }) => {
  return (
    <Card
      hoverable
      className="file-tile"
      actions={[
        <Button
          type="text"
          icon={<DeleteOutlined />}
          onClick={() => onRemove(file)}
          className="delete-button"
        />,
      ]}
    >
      <Card.Meta title={file.name} />
    </Card>
  );
};

FileTile.propTypes = {
  file: PropTypes.object.isRequired,
  onRemove: PropTypes.func.isRequired,
};

export default FileTile;
