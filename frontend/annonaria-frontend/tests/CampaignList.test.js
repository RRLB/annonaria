import { render, screen } from '@testing-library/vue';
import CampaignList from '../src/views/Home.vue';
import axios from 'axios';
import { vi } from 'vitest';

vi.mock('axios');

describe('CampaignList', () => {

    // test 1 get all campaigns
  it('renders campaigns', async () => {
    const campaigns = [
      { id: 1, name: 'Test Campaign', description: 'Test', start_date: '2026-01-01', end_date: '2026-12-31', budget: 10000, is_active: true }
    ];
    axios.get.mockResolvedValue({ data: campaigns });
    localStorage.setItem('token', 'fake-token');

    render(CampaignList);
    await screen.findByText('Test Campaign');
    expect(screen.getByText('Test Campaign')).toBeInTheDocument();
    expect(screen.getByText('Active')).toBeInTheDocument();
  });

  // test 2 error get all campaigns
  it('shows error if unauthorized', async () => {
    axios.get.mockRejectedValue({ response: { status: 401 } });
    localStorage.removeItem('token');

    render(CampaignList);
    await screen.findByText('Failed to fetch campaigns. Please log in.');
    expect(screen.getByText('Failed to fetch campaigns. Please log in.')).toBeInTheDocument();
  });
});