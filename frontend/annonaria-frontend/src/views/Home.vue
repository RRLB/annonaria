<template>
  <div>
    <h1>Campaigns</h1>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Responsive grid for campaign cards -->
    <div class="row">
      <div class="col-12 col-md-6 col-lg-4" v-for="campaign in campaigns" :key="campaign.id">
        <CampaignCard
          :campaign="campaign"
          @edit="editCampaign"
          @delete="deleteCampaign"
          @toggle="toggleCampaign"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CampaignCard from './CampaignCard.vue';
 // Import the card component

export default {
  name: 'HomeView',
  components: { CampaignCard }, // Register the card component
  data() {
    return {
      campaigns: [],
      error: null
    };
  },
  async created() {
    try {
      const response = await axios.get('http://localhost:4000/api/v1/campaigns', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      this.campaigns = response.data;
    } catch (err) {
      this.error = 'Failed to fetch campaigns. Please log in.';
    }
  },
  methods: {
    editCampaign(id) {
      this.$router.push(`/edit/${id}`);
    },
    async deleteCampaign(id) {
      if (confirm('Are you sure you want to delete this campaign?')) {
        try {
          await axios.delete(`http://localhost:4000/api/v1/campaigns/${id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.campaigns = this.campaigns.filter(c => c.id !== id);
        } catch (err) {
          this.error = 'Failed to delete campaign';
        }
      }
    },
    async toggleCampaign(id) {
      try {
        await axios.patch(`http://localhost:4000/api/v1/campaigns/${id}/toggle`, null, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        const campaign = this.campaigns.find(c => c.id === id);
        campaign.is_active = !campaign.is_active;
      } catch (err) {
        this.error = 'Failed to toggle campaign';
      }
    }
  }
};
</script>

<style scoped>
/* You can customize the card and layout here */
.row {
  margin-top: 20px;
}

.card {
  margin-bottom: 20px;
}

.card-body {
  padding: 15px;
}
</style>
