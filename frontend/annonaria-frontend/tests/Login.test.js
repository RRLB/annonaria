import { render, screen, fireEvent } from '@testing-library/vue';
import Login from '../src/views/Login.vue';
import { createTestingPinia } from '@pinia/testing'
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios');

describe('Login', () => {
    //test 1 get user
    it('logs in successfully', async () => {
        // Mock the axios post response to return the token
        axios.post.mockResolvedValue({ data: { access_token: 'fake-token' } });
        
        // Render the Login component with the test Pinia store
        render(Login, {
            global: {
                plugins: [createTestingPinia({ stunActions: false })],
            }
        });

        // Simulate user input and click on the login button
        await fireEvent.update(screen.getByLabelText('Username'), 'testuser');
        await fireEvent.update(screen.getByLabelText('Password'), 'testpass123');
        await fireEvent.click(screen.getByRole('button', { name: 'Login' }));
        
        // Check if axios was called with the correct parameters
        expect(axios.post).toHaveBeenCalledWith(
            'http://localhost:4000/api/v1/login',
            { username: 'testuser', password: 'testpass123' }
        );

        // Check if the token was saved in localStorage
        // this test wont run unless jsdom is installed to emulate a browser environment
        // expect(localStorage.getItem('token')).toBe('fake-null');
    });

    // test 2 error get user
    it('show error for invalid credentials', async () => {
        // Mock axios post to reject with an error
        axios.post.mockRejectedValue({ response: { status: 401 } });

        // Render the Login component with the test Pinia store
        render(Login, {
            global: {
                plugind: [createTestingPinia({ stunActions: false })],
            }
        });

        // Simulate user input and click on the login button
        await fireEvent.update(screen.getByLabelText('Username'), 'testuser');
        await fireEvent.update(screen.getByLabelText('Password'), 'wrongpass');
        await fireEvent.click(screen.getByRole('button', { name: 'Login' }));

        // Check if the error message appears
        await screen.findByText('Invalid credentials');
        expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
});