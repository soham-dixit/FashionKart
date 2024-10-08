import React, { useEffect } from 'react'
import { Box, Typography, styled, Table, TableBody, TableRow, TableCell } from '@mui/material';
import { LocalOffer as Badge } from '@mui/icons-material';
import img1 from './image1.png'
import img2 from './image.png'
import img3 from './image3.png'
import fassured from './fass.svg'

const SmallText = styled(Box)`
    font-size: 14px;
    vertical-align: baseline;
    & > p {
        font-size: 14px;
        margin-top: 10px;
    }
`

const StyledBadge = styled(Badge)`
    margin-right: 10px;
    color: #00cc00;
    font-size: 15px;
`

const ColumnText = styled(TableRow)`
    font-size: 14px;
    vertical-align: baseline;
    & > td {
        font-size: 14px;
        margin-top: 10px;
        border: none;
    }
`

const ProductDetail = ({ product }) => {

    // const fassured = 'https://static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/fa_62673a.png';

    // const supercoin = 'https://rukminim1.flixcart.com/lockin/774/185/images/CCO__PP_2019-07-14.png?q=50';

    const date = new Date(new Date().getTime() + (5 * 24 * 60 * 60 * 1000))

    return (
        <>
            <Typography> {product?.product_display_name} </Typography>

            <Typography style={{ marginTop: 5, color: '#878787', fontSize: 14 }}>
                <Box display="flex" alignItems="center">
                    8 Ratings and 1 Review
                    <Box component="span" style={{ display: 'flex', alignItems: 'center' }}>
                        <img src={fassured} alt="fassured" style={{ width: 25, marginLeft: 15 }} />
                    </Box>
                </Box>
            </Typography>
            <Typography>
                <Box component='span' style={{ fontSize: 28 }}>₹{product?.price}</Box>&nbsp;&nbsp;&nbsp;
                <Box component='span' style={{ color: '#388E3C' }}>{product?.category}</Box>
            </Typography>
            <Typography>Available Offers</Typography>
            <SmallText>
                <Typography><StyledBadge />5% Cashback on Axis Bank Card T&C</Typography>
                <Typography ><StyledBadge />Buy this Product and Get Extra ₹500 Off on Two-Wheelers T&C</Typography>
                <Typography><StyledBadge />Get GST Invoice Available & Save up to 28% for Business purchases on Electronics Know More</Typography>
                <Typography><StyledBadge />Buy this product and get upto ₹500 off on Furniture</Typography>
                <Typography><StyledBadge />Sign up for Pay Later and get Gift Card worth up to ₹500* Know More</Typography>
            </SmallText>

            <Table>
                <TableBody>
                    <ColumnText>
                        <TableCell style={{ color: '#878787' }}>Delivery</TableCell>
                        <TableCell style={{ fontWeight: 600 }}>Delivery by {date.toDateString()} | ₹40</TableCell>
                    </ColumnText>

                    <ColumnText>
                        <TableCell style={{ color: '#878787' }}>Warranty</TableCell>
                        <TableCell>1 Year</TableCell>
                    </ColumnText>

                    <ColumnText>
                        <TableCell style={{ color: '#878787' }}>Seller</TableCell>
                        <TableCell>
                            <Box style={{ color: '#2874f0' }} component='span'>SuperComNet</Box>
                            <Typography>GST Invoice Available</Typography>
                        </TableCell>
                    </ColumnText>

                    <ColumnText>
                        <TableCell colSpan={2}>
                            {/* <img src={img1} alt="" style={{width: 390}}/> */}
                            <img src={img2} alt="" style={{ width: 390, paddingBottom: '2px' }} />
                            <img src={img3} alt="" style={{ width: 390, marginLeft: '10px' }} />
                        </TableCell>
                    </ColumnText>

                    <ColumnText>
                        <TableCell style={{ color: '#878787' }}>Quote:</TableCell>
                        <TableCell>"Style is a way to say who you are without having to speak." - Rachel Zoe
                        </TableCell>
                    </ColumnText>

                </TableBody>
            </Table>
        </>
    )
}

export default ProductDetail