FROM eu.gcr.io/cf-rungis-exp-development-4l/odoofinal:latest
MAINTAINER LNKAsia Techsol LLP. <support@lnkasia.com>

# Copy entrypoint script and Odoo configuration file
COPY ./entrypoint.sh /
COPY ./odoo.conf /etc/odoo/

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

COPY wait-for-psql.py /usr/local/bin/wait-for-psql.py

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]