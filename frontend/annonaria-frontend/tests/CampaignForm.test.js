import { render, screen, fireEvent } from '@testing-library/vue';
import CampaignForm from '../src/views/CampaignForm.vue';
import axios from 'axios';
import { describe, vi } from 'vitest';

vi.mock('axios');

describe('CampaignForm', () => {
    // test 1 create
    it('submits new campaign', async () => {
        axios.post.mockResolvedValue({ data: {} });
        localStorage.setItem('token', 'fake-token');

        render(CampaignForm);
        await fireEvent.update(screen.getByLabelText('Name'), 'Test Campaign');
        await fireEvent.update(screen.getByLabelText('Start Date'), '2026-01-01');
        await fireEvent.update(screen.getByLabelText('End Date'), '2026-12-31');
        await fireEvent.update(screen.getByLabelText('Budget'), '10000');
        await fireEvent.click(screen.getByText('Create'));

        expect(axios.post).toHaveBeenCalledWith(
            'http://localhost:4000/api/v1/campaigns',
            expect.objectContaining({ name: 'Test Campaign' }),
            expect.any(Object)
        );
    });

    // test 2 error creating
    it('shows error for invalid submission', async () => {
        axios.post.mockRejectedValue({ response: { data: { errors: { end_date: ['End date must be after start date.'] } } } });
        localStorage.setItem('token', 'fake-token');

        render(CampaignForm);
        await fireEvent.update(screen.getByLabelText('Name'), 'Invalid Campaign');
        await fireEvent.update(screen.getByLabelText('Start Date'), '2026-06-12');
        await fireEvent.update(screen.getByLabelText('End Date'), '2025-11-10');
        await fireEvent.update(screen.getByLabelText('Budget'), '10000');
        await fireEvent.click(screen.getByText('Create'));

        await screen.findByText((text) => text.includes('End date must be after start date'));
        expect(screen.getByText((text) => text.includes('End date must be after start date'))).toBeInTheDocument();
    });
});