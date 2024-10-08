import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button, Box } from '@mui/material';

function CustomDialog({ open, handleClose, handleAccept, title, message, type }) {
  return (
    <Dialog   open={open} onClose={handleClose}>
      <Box sx={{ padding: '5px' }} >
        <DialogTitle>{title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            {message}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          {type === 'info' ? 
          <Button variant='contained' onClick={handleClose} color="primary">
            OK
          </Button>
          :
          <>
          <Button variant='contained' onClick={handleClose} color="error">
            Abbrechen
          </Button>
          <Button variant='contained' onClick={handleAccept} color="success">
            Bestätigen
          </Button>
          </>
          }
        </DialogActions>
      </Box>
    </Dialog>
  );
}

export default CustomDialog;