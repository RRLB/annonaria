<template>
    <div>
      <h1>{{ isEdit ? 'Edit Campaign' : 'Create Campaign' }}</h1>
      <div v-if="error" class="alert alert-danger">{{ error }}</div>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input v-model="form.name" type="text" class="form-control" id="name" required maxlength="100">
        </div>
        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea v-model="form.description" class="form-control" id="description"></textarea>
        </div>
        <div class="mb-3">
          <label for="start_date" class="form-label">Start Date</label>
          <input v-model="form.start_date" type="date" class="form-control" id="start_date" required>
        </div>
        <div class="mb-3">
          <label for="end_date" class="form-label">End Date</label>
          <input v-model="form.end_date" type="date" class="form-control" id="end_date" required>
        </div>
        <div class="mb-3">
          <label for="budget" class="form-label">Budget</label>
          <input v-model.number="form.budget" type="number" step="0.01" class="form-control" id="budget" required>
        </div>
        <div class="mb-3 form-check">
          <input v-model="form.is_active" type="checkbox" class="form-check-input" id="is_active">
          <label for="is_active" class="form-check-label">Active</label>
        </div>
        <button type="submit" class="btn btn-primary">{{ isEdit ? 'Update' : 'Create' }}</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CampaignForm',
    props: {
      id: String
    },
    data() {
      return {
        form: {
          name: '',
          description: '',
          start_date: '',
          end_date: '',
          budget: 0,
          is_active: false
        },
        error: null,
        isEdit: !!this.id
      };
    },
    async created() {
      if (this.isEdit) {
        try {
          const response = await axios.get(`http://localhost:4000/api/v1/campaigns/${this.id}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.form = response.data;
        } catch (err) {
          this.error = 'Failed to fetch campaign';
        }
      }
    },
    methods: {
      async submitForm() {
        try {
          // Remove id from the form data before sending the request
          // partial id used in the backend to avoid updating or changing the id
          const formData = { ...this.form };
          delete formData.id;

          const url = this.isEdit
            ? `http://localhost:4000/api/v1/campaigns/${this.id}`
            : 'http://localhost:4000/api/v1/campaigns';
          const method = this.isEdit ? 'put' : 'post';

          const response = await axios[method](url, formData, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.$router.push('/');
        } catch (err) {
          this.error = err.response?.data?.errors || 'Failed to save campaign';
        }
      }
    }
  };
  </script>