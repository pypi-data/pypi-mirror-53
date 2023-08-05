import * as React from 'react';

import Dashboard from '../containers/Dashboard';
import Login from './Login';
import { Paper, createMuiTheme, MuiThemeProvider } from '@material-ui/core';
import { colors } from '@material-ui/core';
import { appData } from '../tools';
import ConfirmDialog from '../containers/ConfirmDialog';
import Notification from '../containers/Notification';

const lightTheme = createMuiTheme({
    palette: {
        type: 'light',
        primary: colors.blue,
    },
    typography: {
    }
});

const darkTheme = createMuiTheme({
    palette: {
        type: 'dark',
        primary: colors.cyan,
        secondary: colors.pink,
    },
    typography: {
    }
});

// #006699

type Props = {
    isDarkTheme: boolean,
}

export default React.memo((props: Props) => {
    let { isDarkTheme } = props;
    return (
        <MuiThemeProvider theme={isDarkTheme ? darkTheme : lightTheme}>
            <Paper style={{ height: '100%' }}>
                <Notification />
                {appData.isLoggedIn ? <Dashboard /> : <Login />}
                <ConfirmDialog />
            </Paper>
        </MuiThemeProvider>
    )
})
