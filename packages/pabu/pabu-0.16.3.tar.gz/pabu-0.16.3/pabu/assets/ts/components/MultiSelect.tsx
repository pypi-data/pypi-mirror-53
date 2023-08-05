import * as React from 'react';
import clsx from 'clsx';
import Select from 'react-select';
import Creatable from 'react-select/creatable';

import {Chip, MenuItem, Paper, TextField, Typography} from '@material-ui/core';

import CancelIcon from '@material-ui/icons/Cancel';

import { emphasize, makeStyles, useTheme } from '@material-ui/core/styles';


const useStyles = makeStyles(theme => ({
    input: {
        display: 'flex',
        padding: 0,
        height: 'auto',
    },
    valueContainer: {
        display: 'flex',
        flexWrap: 'wrap' as 'wrap',
        flex: 1,
        alignItems: 'center',
        overflow: 'hidden',
    },
    chip: {
        margin: theme.spacing(0.5, 0.25),
    },
    chipFocused: {
        backgroundColor: emphasize(
            theme.palette.type === 'light' ? theme.palette.grey[300] : theme.palette.grey[700],
            0.08,
        ),
    },
    noOptionsMessage: {
        padding: theme.spacing(1, 2),
    },
    singleValue: {
        fontSize: 16,
    },
    placeholder: {
        position: 'absolute' as 'absolute',
        left: 2,
        bottom: 6,
        fontSize: 16,
    },
    paper: {
        position: 'absolute' as 'absolute',
        zIndex: 1,
        marginTop: theme.spacing(1),
        left: 0,
        right: 0,
    },
    divider: {
        height: theme.spacing(2),
    },
}));

function NoOptionsMessage(props) {
    return (
        <Typography
            color="textSecondary"
            className={props.selectProps.classes.noOptionsMessage}
            {...props.innerProps}
        >
            {props.children}
        </Typography>
    );
}

function inputComponent({inputRef, ...props}) {
    return <div ref={inputRef} {...props} />;
}

function Control(props) {
    const {
        children,
        innerProps,
        innerRef,
        selectProps: {classes, TextFieldProps},
    } = props;

    return (
        <TextField
            fullWidth
            InputProps={{
                inputComponent,
                inputProps: {
                    className: classes.input,
                    ref: innerRef,
                    children,
                    ...innerProps,
                },
            }}
            {...TextFieldProps}
        />
    );
}

function Option(props) {
    return (
        <MenuItem
            ref={props.innerRef}
            selected={props.isFocused}
            component="div"
            style={{
                fontWeight: props.isSelected ? 500 : 400,
            }}
            {...props.innerProps}
        >
            {props.children}
        </MenuItem>
    );
}

function Placeholder(props) {
    const {selectProps, innerProps = {}, children} = props;
    return (
        <Typography color="textSecondary" className={selectProps.classes.placeholder} {...innerProps}>
            {children}
        </Typography>
    );
}


function SingleValue(props) {
    return (
        <Typography className={props.selectProps.classes.singleValue} {...props.innerProps}>
            {props.children}
        </Typography>
    );
}

function ValueContainer(props) {
    return <div className={props.selectProps.classes.valueContainer}>{props.children}</div>;
}

function MultiValue(props) {
    return (
        <Chip
            tabIndex={-1}
            label={props.children}
            className={clsx(props.selectProps.classes.chip, {
                [props.selectProps.classes.chipFocused]: props.isFocused,
            })}
            onDelete={props.removeProps.onClick}
            deleteIcon={<CancelIcon {...props.removeProps} fontSize="small" style={{marginLeft: -5, marginRight: 2}} />}
            size="small"
        />
    );
}

function Menu(props) {
    return (
        <Paper square className={props.selectProps.classes.paper} {...props.innerProps} style={{zIndex: 8000}}>
            {props.children}
        </Paper>
    );
}

const components = {
    Control,
    Menu,
    MultiValue,
    NoOptionsMessage,
    Option,
    Placeholder,
    SingleValue,
    ValueContainer,
};


export type Option = {
    value: any,
    label: string,
}

export type Props = {
    values: Array<Option>,
    options: Array<Option>,
    onChange: (vals: Array<Option>) => void,
    label?: string,
    placeholder?: string,
    creatable?: boolean,
    style?: React.CSSProperties,
};

export default function MultiSelect(props: Props) {
    const classes = useStyles({});

    const theme = useTheme();

    const {values, options, onChange, label, placeholder = false, creatable = false, style = {}} = props;

    const selectStyles = {
        input: base => ({
            ...base,
            color: theme.typography.body1.color,
            '& input': {
                font: 'inherit',
            },
        }),
    };

    const Comp: any = creatable ? Creatable : Select;

    return (
        <Comp
            classes={classes}
            styles={selectStyles}
            style={style}
            inputId="react-select-multiple"
            TextFieldProps={{
                label,
                InputLabelProps: {
                    htmlFor: 'react-select-multiple',
                    shrink: true,
                },
            }}
            placeholder={placeholder}
            options={options}
            components={components}
            value={values}
            onChange={v => onChange(v ? v : [])}
            isMulti
        />
    );
}
