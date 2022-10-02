FROM eu.gcr.io/cf-rungis-exp-development-4l/odoofinal:latest
MAINTAINER LNKAsia Techsol LLP. <support@lnkasia.com>

# Copy Odoo configuration file
COPY ./odoo.conf /etc/odoo/

# Setting up code directory
RUN mkdir -p /mnt/apps
RUN chown -R odoo /mnt/apps
COPY /development/ /mnt/apps/
RUN ls -l /mnt/apps/
# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]