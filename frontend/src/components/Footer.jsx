import React from 'react';
import { Box, Container, Typography, Link, Grid } from '@mui/material';
import { GitHub, LinkedIn, Email } from '@mui/icons-material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 4,
        px: 2,
        mt: 'auto',
        backgroundColor: 'primary.main',
        color: 'white'
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 700 }}>
              🌾 Smart Farmer
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              AI-powered agricultural decision support system for Maharashtra farmers.
              Helping farmers make data-driven decisions for better yields.
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Quick Links
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
              <Link href="/" color="inherit" underline="hover">
                Dashboard
              </Link>
              <Link href="/crop-recommendation" color="inherit" underline="hover">
                Crop Recommendation
              </Link>
              <Link href="/district-insights" color="inherit" underline="hover">
                District Insights
              </Link>
              <Link href="/crop-comparison" color="inherit" underline="hover">
                Crop Comparison
              </Link>
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              Contact & Support
            </Typography>
            <Typography variant="body2" sx={{ mb: 2, opacity: 0.9 }}>
              For technical support or inquiries about the system.
            </Typography>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <GitHub sx={{ cursor: 'pointer', '&:hover': { opacity: 0.7 } }} />
              <LinkedIn sx={{ cursor: 'pointer', '&:hover': { opacity: 0.7 } }} />
              <Email sx={{ cursor: 'pointer', '&:hover': { opacity: 0.7 } }} />
            </Box>
          </Grid>
        </Grid>
        
        <Box sx={{ mt: 4, pt: 3, borderTop: '1px solid rgba(255,255,255,0.2)' }}>
          <Typography variant="body2" align="center" sx={{ opacity: 0.8 }}>
            © 2025 Smart Farmer Recommender System. Built with ❤️ for Maharashtra farmers.
          </Typography>
          <Typography variant="caption" align="center" display="block" sx={{ mt: 1, opacity: 0.7 }}>
            Powered by Machine Learning | Random Forest & Neural Networks
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;
