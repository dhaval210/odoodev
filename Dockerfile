FROM eu.gcr.io/cf-rungis-exp-development-4l/odoofinal
MAINTAINER LNKAsia Techsol LLP. <support@lnkasia.com>

# Copy Odoo configuration file
COPY ./odoo.conf /etc/odoo/

# Setting up code directory
RUN tar -cf /development/transfer.tar .
COPY /development/transfer.tar /mnt/transfer/transfer.tar

# Expose Odoo services
EXPOSE 8069 8071 8072

# Set the default config file
ENV ODOO_RC /etc/odoo/odoo.conf

ENTRYPOINT ["/entrypoint.sh"]
CMD ["odoo"]
RUN tar -xvf /mnt/transfer/transfer.tar /mnt/filestore/addons/.