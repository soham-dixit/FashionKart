import { useState, useContext } from 'react';
import "./cart.css";

import { Box, Button, Typography, styled, Badge } from '@mui/material';
import React from 'react';
import { ShoppingCart } from '@mui/icons-material/';
import LoginDialog from '../login/LoginDialog';
import InventoryIcon from '@mui/icons-material/Inventory';

import { DataContext } from '../../context/DataProvider';
import Profile from './Profile';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

const Wrapper = styled(Box)(({ theme }) => ({
    margin: '0 3% 0 auto',
    display: 'flex',
    // margin: 'auto',
    '& > *': {
        marginRight: '40px !important',
        textDecoration: 'none',
        fontSize: 14,
        alignItems: 'center',
        [theme.breakpoints.down('md')]: {
            // color: '#2874f0',
            display: 'block',
            alignItems: 'center',
            display: 'flex',
            marginTop: 10
        },
    },
    [theme.breakpoints.down('md')]: {
        display: 'block'
    }
}));
const Container = styled(Link)(({ theme }) => ({
    display: 'flex',
    textDecoration: 'none',
    color: 'inherit',
    [theme.breakpoints.down('md')]: {
        display: 'block'
    }
}));


const LoginButton = styled(Button)(({ theme }) => ({
    color: '#2874f0',
    background: '#FFFFFF',
    textTransform: 'none',
    fontWeight: 600,
    borderRadius: 2,
    padding: '5px 25px',
    height: 32,
    boxShadow: 'none',
    [theme.breakpoints.down('md')]: {
        background: '#2874f0',
        color: '#FFFFFF'
    }
}));

const CustomButtons = () => {

    const [open, setOpen] = useState(true);
    const { user } = useSelector(state => state.user)

    const { account, setAccount } = useContext(DataContext);

    const openDialog = () => {
        setOpen(true);
    }

    const { cartItems } = useSelector(state => state.cart);

    return (
        <Wrapper>
            {
                user ? <Profile account={user} setAccount={setAccount} /> :
                    <LoginButton variant='contained' onClick={() => openDialog()} >Login</LoginButton>
            }

            <Container to='/orders' >
                <InventoryIcon />
                <Typography style={{ marginLeft:10, marginTop: 3, width: 135, cursor: 'pointer' }}>My Orders</Typography>
            </Container>
            {/* <Typography style={{ marginTop: 3 }}>More</Typography>
            
            
            */}

            <Container to='/cart'>
                {/* <Badge  badgeContent={cartItems?.length} color='primary'>
                    <ShoppingCart />
                </Badge> */}
                <Badge
                    badgeContent={cartItems?.length}
                    classes={{ badge: 'custom-badge' }} // Apply the custom CSS class
                >
                    <ShoppingCart />
                </Badge>
                <Typography style={{ marginLeft: 10 }}>Cart</Typography>
            </Container>
            {/* <LoginDialog open={open} setOpen={setOpen} /> */}
        </Wrapper>
    )
}

export default CustomButtons
