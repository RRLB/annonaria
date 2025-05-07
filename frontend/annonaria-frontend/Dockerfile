# Use a Node.js image
FROM node:18

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if exists) to the container
COPY package*.json ./

# Install dependencies inside the container
RUN npm install

# Copy the rest of your application files
COPY . .

# Expose the port that your app runs on
EXPOSE 5173

# Command to run your application
CMD ["npm", "run", "dev", "--", "--host"]
