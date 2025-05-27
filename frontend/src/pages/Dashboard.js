import React from 'react';
import { Box, Typography, Container, Grid, Paper } from '@mui/material';
import { useSelector } from 'react-redux';

const Dashboard = () => {
  const { user } = useSelector((state) => state.auth);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Рабочий стол
      </Typography>
      <Grid container spacing={3}>
        {/* Общая информация о задолженности */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: '#e3f2fd',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Задолженность
            </Typography>
            <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
              0 ₽
            </Typography>
          </Paper>
        </Grid>
        
        {/* Стоимость услуг FBS */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: '#e8f5e9',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Услуги FBS
            </Typography>
            <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
              0 ₽
            </Typography>
          </Paper>
        </Grid>
        
        {/* Заказы */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: '#fff3e0',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Заказы
            </Typography>
            <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
              0
            </Typography>
          </Paper>
        </Grid>
        
        {/* Поставки */}
        <Grid item xs={12} md={6} lg={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
              bgcolor: '#f3e5f5',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Поставки
            </Typography>
            <Typography variant="h4" component="div" sx={{ flexGrow: 1 }}>
              0
            </Typography>
          </Paper>
        </Grid>
        
        {/* Последние действия */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Последние действия
            </Typography>
            <Box sx={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Typography variant="body1" color="text.secondary">
                Нет данных для отображения
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
