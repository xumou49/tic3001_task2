import logo from './logo.svg';
import './App.css';
// import {Table, Button} from 'antd';
import axios from 'axios';
import React, { useState, useEffect, useRef, useContext } from 'react';
import { Table, Popconfirm, Button, Form, Input, Typography, InputNumber } from 'antd';


const EditableCell = ({
    editing,
    dataIndex,
    title,
    inputType,
    record,
    index,
    children,
    ...restProps
}) => {
    const inputNode = inputType === 'number' ? <InputNumber /> : <Input />;
    return (
        <td {...restProps}>
            {editing ? (
                <Form.Item
                    name={dataIndex}
                    style={{
                        margin: 0,
                    }}
                    rules={[
                        {
                            required: true,
                            message: `Please Input ${title}!`,
                        },
                    ]}
                >
                    {inputNode}
                </Form.Item>
            ) : (
                children
            )}
        </td>
    );
};
const App = () => {
    const [form] = Form.useForm();
    const [data, setData] = useState([]);
    const [editingKey, setEditingKey] = useState('');
    const isEditing = (record) => record.key === editingKey;
    useEffect(() => {
        axios.get('http://127.0.0.1:5000/api/user-list/users')
            .then(res => {
                setData(res.data['users'].map(u => ({
                    key: u.id,
                    name: u.name,
                    age: u.age,
                    birthday: u.birthday,
                    email: u.email,
                    university: u.university,
                    address: u.address,
                    postcode: u.postcode
                })));
            })
            .catch(err => {
                console.error(err);
            });
    }, []);

    const updateUser = (id, item) => {
        return axios.put(`http://127.0.0.1:5000/api/user-list/users/${id}`, item)
            .then(response => response.data)
            .catch(error => {
                console.error(error);
                throw error;
            });
    }

    const edit = (record) => {
        form.setFieldsValue({
            name: '',
            age: '',
            address: '',
            birthday: '',
            email: '',
            university: '',
            postcode: '',
            ...record,
        });
        setEditingKey(record.key);
    };

    const cancel = () => {
        setEditingKey('');
    };

    const save = async (key) => {
        try {
            const row = await form.validateFields();
            const newData = [...data];
            const index = newData.findIndex((item) => key === item.key);
            if (index > -1) {
                const item = newData[index];
                const newItem = {
                    ...item,
                    ...row,
                }
                delete newItem.key
                const updated = await updateUser(item.key, newItem)
                newData.splice(index, 1, updated.users);
                setData(newData);
                setEditingKey('');
            } else {
                // newData.push(row);
                // setData(newData);
                // setEditingKey('');
                console.log('Index not found');
            }
        } catch (errInfo) {
            console.log('Validate Failed:', errInfo);
        }
    };

    const columns = [
        {
            title: 'Name', width: 100, dataIndex: 'name', key: 'name', fixed: 'left', editable: true,
        },
        {
            title: 'Age', width: 100, dataIndex: 'age', key: 'age', fixed: 'left', sorter: true, editable: true,
        },
        {
            title: 'Birthday', dataIndex: 'birthday', key: 'birthday', editable: true,
        },
        {
            title: 'Email', dataIndex: 'email', key: 'email', editable: true,
        },
        {
            title: 'University', dataIndex: 'university', key: 'university', editable: true,
        },
        {
            title: 'Address', dataIndex: 'address', key: 'address', editable: true,
        },

        {
            title: 'Postcode', dataIndex: 'postcode', key: 'postcode', editable: true,
        },
        {
            title: 'Edit', key: 'edit', dataIndex: 'edit', fixed: 'right', width: 200,
            render: (_, record) => {
                const editable = isEditing(record);
                return editable ? (
                    <span>
                        <Typography.Link
                            onClick={() => save(record.key)}
                            style={{
                                marginRight: 8,
                            }}
                        >
                            Save
                        </Typography.Link>
                        <Popconfirm title="Sure to cancel?" onConfirm={cancel}>
                            <a>Cancel</a>
                        </Popconfirm>
                    </span>
                ) : (
                    <Typography.Link disabled={editingKey !== ''} onClick={() => edit(record)}>
                        Edit
                    </Typography.Link>
                );
            },
        },
    ];
    const mergedColumns = columns.map((col) => {
        if (!col.editable) {
            return col;
        }
        return {
            ...col,
            onCell: (record) => ({
                record,
                inputType: col.dataIndex === 'age' ? 'number' : 'text',
                dataIndex: col.dataIndex,
                title: col.title,
                editing: isEditing(record),
            }),
        };
    });
    return (
        <div>
            <Form form={form} component={false}>
                <Table
                    components={{
                        body: {
                            cell: EditableCell,
                        },
                    }}
                    // columns={columns}
                    columns={mergedColumns}
                    dataSource={data}
                    bordered
                    size="large"
                    rowClassName="editable-row"
                    pagination={{
                        onChange: cancel,
                    }}
                // scroll={{x: 1300,}}
                />
            </Form>
        </div>
    )
};

export default App;
//
// function App() {
//     return (
//         <div className="App">
//             return (
//             <Table columns={columns} dataSource={data}/>
//             );
//         </div>
//     );
// }
//
// export default App;
