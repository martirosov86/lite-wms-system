import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

const NotFound = () => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
      }}
    >
      <Typography variant="h1" component="h1" gutterBottom>
        404
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>
        Страница не найдена
      </Typography>
      <Typography variant="body1" sx={{ mb: 4 }}>
        Запрашиваемая страница не существует или была удалена.
      </Typography>
      <Button variant="contained" component={RouterLink} to="/dashboard">
        Вернуться на главную
      </Button>
    </Box>
  );
};

export default NotFound;
