import React from 'react';
import { List, ListItem, ListItemText, IconButton } from '@material-ui/core';
import CommentIcon from '@material-ui/icons/Comment';
import AssignmentIcon from '@material-ui/icons/Assignment';

const ProductExportCollaboration = ({ products }) => {
  return (
    <List sx={{ padding: '2rem', backgroundColor: '#f9f9f9' }}>
      {products.map(product => (
        <ListItem key={product.id} sx={{ borderBottom: '1px solid #e0e0e0', paddingY: '1rem' }}>
          <ListItemText
            primary={
              <>
                <strong>{product.name}</strong> - HS Code: {product.hsCode}
              </>
            }
            secondary={`Target Regions: ${product.targetRegions.join(', ')} - Status: ${product.status}`}
            sx={{ typography: 'body2', color: '#333' }}
          />
          <IconButton edge="end" aria-label="comment" sx={{ color: '#666', '&:hover': { color: '#007bff' } }}>
            <CommentIcon />
          </IconButton>
          <IconButton edge="end" aria-label="assign task" sx={{ color: '#666', '&:hover': { color: '#007bff' } }}>
            <AssignmentIcon />
          </IconButton>
        </ListItem>
      ))}
    </List>
  );
};

export default ProductExportCollaboration;
