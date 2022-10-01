FROM eu.gcr.io/cf-rungis-exp-development-4l/odoofinal:latest
MAINTAINER LNKAsia Techsol LLP. <support@lnkasia.com>

# Copy Odoo configuration file
COPY ./odoo.conf /etc/odoo/

# Setting up code directory
WORKDIR /mnt/filestore/addons
COPY . /mnt/filestore/addons/.

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]