FROM node:18 AS frontend
COPY front/package.json /var/app/front/package.json
COPY front/package-lock.json /var/app/front/package-lock.json
WORKDIR /var/app/front
RUN npm install
COPY front/src /var/app/front/src
COPY front/public /var/app/front/public
RUN npm run build

FROM python:3.9
COPY --from=frontend /var/app/front/build /var/app/front/build
COPY api/requirements.txt /var/app/api/requirements.txt
WORKDIR /var/app/api
RUN pip install --no-cache-dir --upgrade -r /var/app/api/requirements.txt
COPY api /var/app/api
CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]
