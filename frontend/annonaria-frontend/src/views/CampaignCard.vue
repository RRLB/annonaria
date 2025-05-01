<template>
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{{ campaign.name }}</h5>
        <p class="card-text-scroll">{{ campaign.description }}</p>
        <p class="card-text">
          <strong>Start:</strong> {{ campaign.start_date }} <br />
          <strong>End:</strong> {{ campaign.end_date }}
        </p>
        <p class="card-text"><strong>Budget:</strong> ${{ campaign.budget }}</p>
  
        <!-- Campaign Status -->
        <p class="card-text">
          <span class="badge" :class="campaign.is_active ? 'badge-active' : 'badge-inactive'">
            {{ campaign.is_active ? 'Active' : 'Inactive' }}
          </span>
        </p>
  
        <!-- Action buttons -->
        <button class="btn btn-sm btn-primary me-1" @click="editCampaign(campaign.id)">Edit</button>
        <button class="btn btn-sm btn-danger me-1" @click="deleteCampaign(campaign.id)">Delete</button>
        <button class="btn btn-sm btn-secondary" @click="toggleCampaign(campaign.id)">
          {{ campaign.is_active ? 'Deactivate' : 'Activate' }}
        </button>
      </div>
    </div>
  </template>
  
  <script>
  import '../assets/campaignCard.css';
  
  export default {
    name: 'CampaignCard',
    props: {
      campaign: Object
    },
    methods: {
      editCampaign(id) {
        this.$emit('edit', id); // Emit edit event to parent
      },
      deleteCampaign(id) {
        this.$emit('delete', id); // Emit delete event to parent
      },
      toggleCampaign(id) {
        this.$emit('toggle', id); // Emit toggle event to parent
      }
    }
  };
  </script>
  