import { createStyles, Slide, Snackbar, Theme, WithStyles, withStyles } from '@material-ui/core';
import { amber, green } from '@material-ui/core/colors';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import ErrorIcon from '@material-ui/icons/Error';
import InfoIcon from '@material-ui/icons/Info';
import WarningIcon from '@material-ui/icons/Warning';
import * as React from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { hideNotification } from '../actions';
import { Notification, State } from '../types';


type StateProps = {
    notification: Notification,
}

type DispatchProps = {
    hideNotification: () => void,
}

const mapStateToProps = (store: State) => ({
    notification: store.notification,
});

const mapDispatchToProps = dispatch => bindActionCreators({ hideNotification }, dispatch);

const styles = (theme: Theme) => createStyles({
    success: {
        backgroundColor: green[600],
    },
    error: {
        backgroundColor: theme.palette.error.dark,
    },
    info: {
        backgroundColor: theme.palette.primary.main,
    },
    warning: {
        backgroundColor: amber[700],
    },
    content: {
        display: 'flex',
        alignItems: 'center',
        color: 'white',
    },
    icon: {
        fontSize: 20,
        marginRight: theme.spacing(1),
    },
})

type Props = StateProps & DispatchProps & WithStyles<typeof styles>;

const variantIcon = {
    success: CheckCircleIcon,
    warning: WarningIcon,
    error: ErrorIcon,
    info: InfoIcon,
};

function SlideTransition(props) {
    return <Slide {...props} direction="down" />;
}

export default connect<StateProps, DispatchProps>(mapStateToProps, mapDispatchToProps)(withStyles(styles)((props: Props) => {

    const { notification, hideNotification, classes } = props;

    const handleClose = (event: React.SyntheticEvent<any>, reason: string) => {
        if (reason === 'clickaway') {
            return;
        }
        hideNotification();
    };

    function Message(props: { data: Notification }) {
        const { message, variant } = props.data;
        const Icon = variantIcon[variant];
        return (<span className={classes.content}><Icon className={classes.icon} />{message}</span>);
    }

    return (
        <Snackbar
            anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
            open={notification.show}
            autoHideDuration={5000}
            onClose={handleClose}
            TransitionComponent={SlideTransition}
            ContentProps={{ className: classes[notification.variant] }}
            message={<Message data={notification} />}
        />
    );
}));
