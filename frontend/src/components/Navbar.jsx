import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Box,
  useMediaQuery,
  useTheme,
  Chip
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import DashboardIcon from '@mui/icons-material/Dashboard';
import AgricultureIcon from '@mui/icons-material/Agriculture';
import ScienceIcon from '@mui/icons-material/Science';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import CompareArrowsIcon from '@mui/icons-material/CompareArrows';
import LocationOnIcon from '@mui/icons-material/LocationOn';
import CloudIcon from '@mui/icons-material/Cloud';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import { useApp } from '../context/AppContext';
import LanguageSelector from './LanguageSelector';

const menuItems = [
  { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
  { text: 'Crop Recommendation', icon: <AgricultureIcon />, path: '/crop-recommendation' },
  { text: 'Nutrient Analysis', icon: <ScienceIcon />, path: '/nutrient-analysis' },
  { text: 'Crop Comparison', icon: <CompareArrowsIcon />, path: '/crop-comparison' },
  { text: 'District Insights', icon: <LocationOnIcon />, path: '/district-insights' },
  { text: 'Weather Planning', icon: <CloudIcon />, path: '/weather-planning' },
  { text: 'Economic Analysis', icon: <AttachMoneyIcon />, path: '/economic-analysis' },
];

const Navbar = () => {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const navigate = useNavigate();
  const { apiStatus } = useApp();

  const toggleDrawer = (open) => (event) => {
    if (event.type === 'keydown' && (event.key === 'Tab' || event.key === 'Shift')) {
      return;
    }
    setDrawerOpen(open);
  };

  const handleNavigation = (path) => {
    navigate(path);
    setDrawerOpen(false);
  };

  const drawer = (
    <Box
      sx={{ width: 280 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <Box sx={{ p: 2, backgroundColor: 'primary.main', color: 'white' }}>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>
          🌾 Smart Farmer
        </Typography>
        <Typography variant="caption">
          Maharashtra Agricultural AI
        </Typography>
      </Box>
      <Box sx={{ p: 2, borderBottom: '1px solid #e0e0e0' }}>
        <LanguageSelector variant="standard" />
      </Box>
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton onClick={() => handleNavigation(item.path)}>
              <ListItemIcon sx={{ color: 'primary.main' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <AppBar position="sticky" elevation={2}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              edge="start"
              onClick={toggleDrawer(true)}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          <Typography
            variant="h6"
            component={Link}
            to="/"
            sx={{
              flexGrow: 1,
              textDecoration: 'none',
              color: 'white',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: 1
            }}
          >
            🌾 Smart Farmer
            {!isMobile && (
              <Typography variant="caption" sx={{ ml: 2, opacity: 0.9 }}>
                Maharashtra Edition
              </Typography>
            )}
          </Typography>

          <Chip
            label={apiStatus === 'connected' ? 'Connected' : 'Offline'}
            color={apiStatus === 'connected' ? 'success' : 'error'}
            size="small"
            sx={{ mr: 2 }}
          />

          {!isMobile && (
            <>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <Button color="inherit" component={Link} to="/">
                  Dashboard
                </Button>
                <Button color="inherit" component={Link} to="/crop-recommendation">
                  Recommend
                </Button>
                <Button color="inherit" component={Link} to="/crop-comparison">
                  Compare
                </Button>
              </Box>
              <Box sx={{ ml: 2 }}>
                <LanguageSelector variant="navbar" />
              </Box>
            </>
          )}

          {isMobile && (
            <Box sx={{ ml: 1 }}>
              <LanguageSelector variant="navbar" />
            </Box>
          )}
        </Toolbar>
      </AppBar>

      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={toggleDrawer(false)}
      >
        {drawer}
      </Drawer>
    </>
  );
};

export default Navbar;
