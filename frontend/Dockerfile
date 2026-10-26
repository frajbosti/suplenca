# osnovna slika z Node.js (enaka glavna različica kot na mojem računalniku)
FROM node:24-slim

# delovna mapa znotraj kontejnerja
WORKDIR /app

# najprej namesti knjižnice iz package.json
COPY package*.json ./
RUN npm install

# nato kopira še vso kodo frontenda
COPY . .

# zažene razvojni strežnik Vite; --host omogoči dostop izven kontejnerja
CMD ["npm", "run", "dev", "--", "--host"]