import React from 'react'
import Appbar from './Appbar'
import styles from './App.module.css';

export default function Layout(props) {
    return (
        <div className={styles.root}>
            <Appbar />
            {props.children}
        </div>
    )
}